# Simulating the Turtlebot2

Decided to do this as I wanted something to do on the train home.

This is a to do list from VS code's agent.

> Recommended development order
>
> 1. Improve the URDF with correct links, joints, visuals, collisions, and inertias.
> 2. Display it in RViz2 using robot_state_publisher.
> 3. Add simulated wheel movement and odometry.
> 4. Add a simulated depth camera.
> 5. Verify /scan through depthimage_to_laserscan.
> 6. Run slam_toolbox and create a map.
> 7. Run Nav2 with your DWB configuration.
> 8. Test goals and obstacle avoidance in a small Gazebo world.
> 9. Replace the simple world with a model of the lab floor.
> 10. Reuse the same Nav2 and SLAM parameters on the real robot.
>
> The most important design choice is to keep the real and simulated systems using the same topic and frame names. Then simulation becomes a test environment for the existing TurtleBot 2 software rather than a separate application that must be maintained independently.

## First visualization test (1,2,3)

The improved URDF can now be checked in RViz2 before adding physics or simulated sensors. Build and source the package, then run:

```bash
colcon build --packages-select turtlebot2_main
source install/setup.bash
ros2 launch turtlebot2_main urdf_rviz.launch.py
```

This starts `robot_state_publisher` with `turtlebot2_se.urdf` and opens the saved RViz2 configuration. The launch file also starts the lightweight differential-drive kinematic simulator. Set RViz2's fixed frame to `odom` to view the moving robot.

The kinematic simulator:

* subscribes to `/cmd_vel`;
* publishes wheel positions on `/joint_states`, which makes the wheel joints move in RViz2;
* publishes `/odom`; and
* publishes the `odom -> base_footprint` transform.

Build and source the package after changing the simulator:

```bash
colcon build --packages-select turtlebot2_main
source install/setup.bash
ros2 launch turtlebot2_main urdf_rviz.launch.py
```

In another terminal, send a short forward command:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
	"{linear: {x: 0.1}, angular: {z: 0.0}}"
```

The simulator stops applying commands after 0.5 seconds without a fresh message. This stage provides kinematics only: it does not yet simulate collisions, wheel slip, or camera data. Those require Gazebo or another physics simulator.

## Add simulated depth camera (4,5)

The first camera simulation uses a lightweight ROS node rather than Gazebo. It
publishes a deterministic Astra-like depth image and camera calibration, so the
same depth-to-laserscan and SLAM pipeline can be exercised before adding a
physics simulator.

Build and source the package:

```bash
colcon build --packages-select turtlebot2_main depthimage_to_laserscan
source install/setup.bash
```

Start the simulated robot, camera, and laser scan pipeline:

```bash
ros2 launch turtlebot2_main simulated_camera.launch.py
```

The simulated camera publishes:

* `/depth/image_raw` as a `sensor_msgs/msg/Image` with `16UC1` millimetre data;
* `/depth/camera_info` as matching `sensor_msgs/msg/CameraInfo`; and
* `/scan` through `depthimage_to_laserscan`.

The image frame is `camera_depth_optical_frame`. The scan is published in
`camera_depth_frame`, using the camera links already defined in
`turtlebot2_se.urdf`.

Check the topics and camera contract from another terminal:

```bash
ros2 topic hz /depth/image_raw
ros2 topic echo /depth/camera_info --once
ros2 topic echo /scan --once
ros2 run tf2_ros tf2_echo base_link camera_depth_optical_frame
```

The default synthetic scene has a 3 m background, a central world-fixed
obstacle at x=2.0 m, and a small invalid border. Its apparent depth therefore
decreases as the robot drives forward. Parameters are in
`turtlebot2_main/config/synthetic_camera.yaml`. The current scene follows only
the robot's forward x position; turning does not yet move the obstacle across
the image. This phase also does not model collisions, optical noise, or
rendered geometry. A future Gazebo camera should replace only the producer
while preserving the `/depth/...` topics and camera frame contract.

## Run SLAM Toolbox (6)

The simulated camera stack can be started together with the synchronous SLAM
Toolbox mapper. Build and source the workspace after changing the launch files:

```bash
colcon build --packages-select turtlebot2_main depthimage_to_laserscan
source install/setup.bash
```

Start the simulated robot, camera, laser scan, RViz2, and SLAM Toolbox:

```bash
ros2 launch turtlebot2_main simulated_slam.launch.py
```

The launch file uses wall time by default because the kinematic simulator does not publish `/clock`. To use a simulator that provides `/clock`, pass:

```bash
ros2 launch turtlebot2_main simulated_slam.launch.py use_sim_time:=true
```

Drive the robot slowly from another terminal so SLAM Toolbox receives scans at different poses:

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist \
	"{linear: {x: 0.1}, angular: {z: 0.0}}"
```

Stop the command with Ctrl-C, then turn the robot and drive another short
segment:

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist \
	"{linear: {x: 0.0}, angular: {z: 0.4}}"
```

Check that the mapper is publishing a map and that scans are still arriving:

```bash
ros2 topic list | grep -E '^/(scan|map)$'
ros2 node list | grep slam_toolbox
ros2 lifecycle get /slam_toolbox
ros2 topic info /scan
ros2 topic echo /scan --once
ros2 topic hz /scan
ros2 run tf2_ros tf2_echo odom camera_depth_frame
ros2 topic echo /map --once
ros2 topic echo /slam_toolbox/graph_visualization --once
```

The map is generated after SLAM Toolbox receives a scan and can resolve the `odom -> camera_depth_frame` transform. If `/scan` is not listed, or the TF check fails, fix that upstream path before checking `/map` again.

Save the map from a separate terminal after exploring the area:

```bash
mkdir -p ~/ws/maps
ros2 run nav2_map_server map_saver_cli -f ~/ws/maps/turtlebot2_sim
```

The current synthetic scene is deterministic and intentionally simple. This validates the scan, odometry, TF, and SLAM wiring; meaningful room-scale maps will require a richer scene model or the planned Gazebo simulation.

## Run Nav2 with your DWB configuration (7)

**DWB** means **Dynamic Window Based** controller, implemented in Nav2 as the
`dwb_core::DWBLocalPlanner` plugin and based on the Dynamic Window Approach
(DWA). It is Nav2's local controller:
given a global path and nearby obstacle data, it samples feasible linear and
angular velocities, scores the resulting short trajectories, and selects a
command that follows the path while avoiding obstacles. It is not the global
planner; Nav2's planner and costmaps supply the path and obstacle information
that DWB uses.

The repository configuration in
[`turtlebot2_main/config/nav2_params.yaml`](turtlebot2_main/config/nav2_params.yaml)
already selects DWB for `FollowPath`, sets lateral velocity to zero for the
differential-drive Kobuki, and caps forward speed at 0.26 m/s. This procedure
loads the map saved in step 6, starts AMCL to localize against it, then starts
the Nav2 navigation servers.

### Prepare the workspace and map

Make sure step 6 produced both files below; use the actual path if you saved
the map somewhere else:

```bash
ls -l ~/ws/maps/turtlebot2_sim.yaml ~/ws/maps/turtlebot2_sim.pgm
```

From the colcon workspace root, rebuild and source the package so Nav2 can
load the installed parameter file:

```bash
colcon build --packages-select turtlebot2_main
source install/setup.bash
```

If Nav2 or its DWB plugin is not installed on this machine:

```bash
sudo apt install ros-${ROS_DISTRO}-nav2-bringup ros-${ROS_DISTRO}-nav2-dwb-controller
```

### Start the simulation and navigation

Stop the step-6 `simulated_slam.launch.py` launch with Ctrl-C first. AMCL will
provide the `map -> odom` transform for this run; do not run SLAM Toolbox at
the same time, since it would also publish that transform.

Use three terminals, sourcing the workspace in each one. In terminal 1 start
the robot, RViz2, simulated camera, and `/scan` pipeline (without SLAM):

```bash
ros2 launch turtlebot2_main simulated_camera.launch.py
```

In terminal 2 load the saved map and start AMCL localization. This simulator
does not publish `/clock`, so keep simulation time disabled:

```bash
ros2 launch nav2_bringup bringup_launch.py \
  slam:=False \
  map:=$HOME/ws/maps/turtlebot2_sim.yaml \
  params_file:=$(ros2 pkg prefix turtlebot2_main)/share/turtlebot2_main/config/nav2_params.yaml \
  use_sim_time:=false
```

At this point, I realised that the map was not working well, so we moved on to the next task. 


## Run the Gazebo simulation (8)

The earlier phases use a kinematic simulator and a synthetic depth camera. This
phase replaces them with Gazebo (`gz sim`), which provides physics, wall and
obstacle collisions, a differential-drive Kobuki model, and a simulated 2D
lidar publishing `/scan`. Gazebo also publishes `/clock`, so every launch file
here uses `use_sim_time:=true` internally.

The files added for this phase are:

* `urdf/turtlebot2_gz.urdf`: the robot with a simulated lidar, the DiffDrive
  plugin (`/cmd_vel` in, `/odom` and `odom -> base_footprint` TF out), and a
  joint state publisher.
* `worlds/turtlebot2_rooms.sdf`: a 10 x 8 m two-room world with two doorways,
  box obstacles, and pillars.
* `launch/gazebo_sim.launch.py`: Gazebo, robot state publisher, robot spawn,
  and the ROS-Gazebo bridge for `/clock`, `/cmd_vel`, `/odom`, `/tf`,
  `/joint_states`, and `/scan`.
* `launch/gazebo_slam.launch.py`: `gazebo_sim.launch.py` plus SLAM Toolbox.
* `launch/gazebo_nav2.launch.py`: `gazebo_sim.launch.py` plus Nav2 with AMCL on
  a saved map.

The lidar is a 360 degree, 12 m scanner mounted 0.14 m above the base. It is
a simulation convenience: the real robot has only the Astra camera, whose
`/scan` is a narrower 5 m field of view. A SLAM map made with this lidar is
therefore not representative of the real sensor.

### Install and build

```bash
sudo apt install ros-${ROS_DISTRO}-ros-gz ros-${ROS_DISTRO}-slam-toolbox \
  ros-${ROS_DISTRO}-nav2-bringup
cd ~/ws
colcon build --packages-select turtlebot2_main
source install/setup.bash
```

### Check the robot and world

Start only Gazebo and the robot, with RViz2 as an optional extra:

```bash
ros2 launch turtlebot2_main gazebo_sim.launch.py
ros2 launch turtlebot2_main gazebo_sim.launch.py rviz:=true
```

The robot spawns at `x=-3.0, y=0.0`. Override it with `x:=... y:=... yaw:=...`.
In another terminal, check that the bridge is working:

```bash
ros2 topic list | grep -E '^/(clock|scan|odom|tf|cmd_vel)$'
ros2 topic hz /scan
ros2 topic echo /odom --once
```

`/scan` should run at about 10 Hz. If the Gazebo window opens but there are no
ROS topics, check that `parameter_bridge` is running in the launch output.

Only one Gazebo instance can use the world name `turtlebot2_world` at a time.
If a previous run is still alive you will see `Another world of the same name
is running`, and SLAM Toolbox or Nav2 will fail on missing TF. Stop the old
launch with Ctrl-C and check `ps aux | grep gz-sim` before starting again.

### Build a map with SLAM Toolbox

```bash
ros2 launch turtlebot2_main gazebo_slam.launch.py
```

SLAM Toolbox starts 12 seconds after Gazebo so that `/clock`, TF, and the
robot are available. Drive the robot through both rooms and the doorways,
slowly, with keyboard tele-op in a second terminal:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Keep linear speed at or below 0.25 m/s and turn gently. Drive back over parts
of the route you have already mapped so SLAM can close loops. Watch the map
grow in RViz2 (fixed frame `map`, `Map` display on `/map`).

When the walls are complete, save the map from a separate terminal:

```bash
mkdir -p ~/ws/maps
ros2 run nav2_map_server map_saver_cli -f ~/ws/maps/turtlebot2_gz --ros-args -p use_sim_time:=true
```

Open `~/ws/maps/turtlebot2_gz.pgm` in a picture editor (I used Gwenview) and check that the walls are closed lines,
both doorways are open, and the obstacles are present. If not, stop the
launch, restart, and re-drive the route. Then stop the SLAM launch with Ctrl-C.

STOPPED HERE!!!!! Test the rest.

### Navigate on the saved map with Nav2

```bash
ros2 launch turtlebot2_main gazebo_nav2.launch.py
```

To use a different map:

```bash
ros2 launch turtlebot2_main gazebo_nav2.launch.py map:=$HOME/ws/maps/my_map.yaml
```

This single launch starts Gazebo, RViz2, and the Nav2 `bringup_launch.py` with
`slam:=False`. That launch file includes the lifecycle manager that activates
`map_server`, `amcl`, the planner, the controller, and the behavior servers.
(`localization_launch.py` on its own does not start a lifecycle manager, so
its nodes stay unconfigured.) After 15 seconds the launch publishes an initial
pose to `/initialpose` that matches the spawn pose. If you changed `x` or `y`,
pass the same values to this launch. Orientation is assumed to be zero.

Do not also run `nav2.launch.py` from earlier phases, because
`gazebo_nav2.launch.py` already starts the navigation servers.

Check the stack:

```bash
ros2 lifecycle get /amcl
ros2 lifecycle get /controller_server
ros2 run tf2_ros tf2_echo map base_footprint
```

Both lifecycle nodes should report `active`. In RViz2, set the fixed frame to
`map`, then use **Nav2 Goal** to send the robot to a point in the other room.
If AMCL has not localized, use **2D Pose Estimate** to correct it.

The Nav2 parameters in `config/nav2_params.yaml` use `use_sim_time: false` for
some servers, but the launch file sets `use_sim_time:=true` globally. Check the
log for time-related warnings if the planner or controller fail to start.

### Known limits

* The Gazebo robot is a simplified model: wheel friction, mass, and the lidar
  are not tuned to the real Kobuki.
* The lidar differs from the real Astra-based scan (see above), so tuning
  done here does not transfer directly.
