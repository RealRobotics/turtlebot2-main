# Running SLAM on TurtleBot 2

## Review of options

Gemini used with prompt "ros2 slam options for a ground robot with a orbbec astra camera and a rpi4 controller"

The RPi4 was specified to force resource constrained conditions similar to the laptop being used for phase 1.

### Answer

Implementing SLAM on a Raspberry Pi 4 (RPi4) with an Orbbec Astra RGB-D camera presents a unique challenge: depth/visual SLAM algorithms are highly memory and CPU intensive, while the RPi4 is a resource-constrained hardware platform.To build a reliable system, you must balance your computing limitations with your mapping goals. The top three ROS 2 SLAM options suited for this specific hardware stack are detailed below.

#### Comparison of ROS 2 SLAM Options

| SLAM Package |Map Type|Performance on RPi4|Recommended Setup/Optimizations|
|---|---|---|---|
|slam_toolbox (Highly Recommended)|2D Occupancy Grid|Excellent (Lightweight)|Convert depth to pseudo-LaserScan (depthimage_to_laserscan).|
|RTAB-Map (Best Feature Set)|2D Grid + 3D OctoMap|Moderate (Needs tuning)|Lower camera resolution, disable 3D cloud publishing, rely heavily on wheel odometry.|
|ORB-SLAM3 (Visual-Only)|Sparse 3D Point Cloud|Poor (High CPU/Memory)|Offload computation via a distributed ROS 2 network to a laptop.|

### Conclusion

Start off with `slam_toolbox` and then try `RTAB-Map`.

## Running

Basic principle is to create individual launch files for each aspect, test and debug.

### Camera

To run the camera, I started off by creating the `astra_camera.launch.py` file and tested the ORBBEC Astra camera.  Uses lots of CPU, about 110% to do the depth and colour camera feeds.  Just using the depth halves this.  The image shown in `rqt` is interesting.  My hand has seven or eight fingers depending on where I hold my hand!

### Kobuki Base

Start the Kobuki base using:

```bash
ros2 launch turtlebot2_main turtlebot2-base.launch.py
```

This works fine.  Now to tele-op this using the keyboard.

Fixed the Kobuki keyboard teleop.  All working.

## SLAM Implementation and testing

These are the steps suggested by Gemini using this prompt:

>Please suggest a development path to incrementally build and test each step needed to acheive the objective of fully mapping the ground floor of my house and returning the starting point when the map is complete.

Seem reasonable to me, so let start.

>To get your TurtleBot2 safely mapping your ground floor autonomously without crashing into furniture, you should follow a 5-stage incremental development path.Testing each layer individually ensures that if something breaks, you know exactly which component is causing the issue.
>
>### Phase 1: Hardware & Sensor Validation (The Foundation)
>
>Before testing any navigation or mapping software, you must ensure your robot can see, feel, and move reliably.
>
>1. Teleoperation Check. Drive the robot around using your keyboard or a joystick (teleop_twist_keyboard). Ensure the Kobuki base moves in the direction you expect and does not drift heavily.
>2. Odometry Calibration. Drive the robot in a straight line for exactly 1 metre. Check the `/odom` topic data. Does the robot think it went 1 metre? Rotate 360 degrees and verify the odometry rotation matches reality.
>3. Depth-to-Laser Conversion. Launch your Astra camera and your `depthimage_to_laserscan` node. Open `Rviz2` and add a LaserScan display. Verify that tables and walls show up as a flat 2D ring of points.
>
>### Phase 2: Manual Mapping (Passive SLAM)
>
>In this phase, you test slam_toolbox while keeping full control over the robot's movements.
>
>4. Launch SLAM. Run your slam_toolbox node alongside your hardware drivers.
>5. Joystick Mapping. Drive the robot very slowly around a single room. In Rviz2, watch the map generate.
>6. Loop Closure Test. Drive out of the room, come back in, and watch the map "snap" into alignment. If the map tears or gets corrupted, your robot is driving too fast, or your camera's frame rate is too low.
>7. Map Saving. Use the nav2_map_server or the Rviz2 slam_toolbox plugin to save your map (map.yaml and map.pgm). Verify the files exist on your disk.
>
>### Phase 3: Assisted Navigation (Active Driving)
>
>Now you introduce Nav2 to control the wheels, but you still choose where the robot goes.
>
>8. Nav2 Integration. Launch your robot drivers, slam_toolbox (in online/sync mode), and the Nav2 stack.
>9. Costmap Verification. In Rviz2, look at the local and global costmaps. Ensure walls have an "inflation layer" (a colorful buffer zone) around them. This is what keeps Nav2 from clipping doorways.
>10. 2D Nav Goal Test. Use the "2D Nav Goal" button at the top of Rviz2 to click a spot across the room. Nav2 should automatically plan a path and drive the TurtleBot2 there while slam_toolbox updates the map actively.
>
>### Phase 4: Autonomous Exploration (The Brain)
>
>With Nav2 working perfectly, you can hand control over to an exploration package to find the frontiers.
>
>11. Install Explore Lite. Clone and compile the ROS 2 version of explore_lite (or your chosen frontier exploration node).
>12. Restricted Boundary Test. Block off a small, safe area (e.g., just your hallway) using boxes. Launch your full stack + explore_lite. Watch the robot autonomously seek out the edges of the hallway until it runs out of frontiers and stops.
>13. Whole Floor Run. Open the doors and let it tackle the entire ground floor. Keep a remote control or a spacebar close by as an emergency stop.Phase 5: Return to Home (The Finish)The final step is triggering the return sequence once the map is complete.
>14. Mark the Home Base. Before the robot moves in Step 13, record its starting coordinates relative to the map frame (usually x: 0.0, y: 0.0).
>15. Script the Homing Sequence. Write a simple Python action client or use a Nav2 Waypoint Follower script.
>16. End-to-End Test. Your script should monitor the explore_lite status. When explore_lite publishes that no more frontiers exist, your script should automatically send a final Nav2 goal to the (0,0) home coordinates.
