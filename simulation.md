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
mkdir -p ~/maps
ros2 run nav2_map_server map_saver_cli -f ~/maps/turtlebot2_sim
```

The current synthetic scene is deterministic and intentionally simple. This validates the scan, odometry, TF, and SLAM wiring; meaningful room-scale maps will require a richer scene model or the planned Gazebo simulation.
