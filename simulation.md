# Simulating the Turtlebot2

Decided to do this as I wanted something to do on the train home.

This is a to do list from VS code's agent.

> Recommended development order
>
> * Improve the URDF with correct links, joints, visuals, collisions, and inertias.
> * Display it in RViz2 using robot_state_publisher.
> * Add simulated wheel movement and odometry.
> * Add a simulated depth camera.
> * Verify /scan through depthimage_to_laserscan.
> * Run slam_toolbox and create a map.>
> * Run Nav2 with your DWB configurati> on.>
> * Test goals and obstacle avoidance > in > a small Gazebo world.>
> * Replace the simple world with a mo> del>  of the ground floor.>
> * Reuse the same Nav2 and SLAM param> ete> rs on the real robot.>
>
> The most important design choice is to keep the real and sim> ulated systems using the same topic and frame names. Then simulation becomes a test environment for the existing TurtleBot 2 software rather than a separate application that must be maintained independently.

## First visualization test

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
