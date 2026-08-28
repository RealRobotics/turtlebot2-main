# Running SLAM on TurtleBot 2

## To do list 

Gemini has compiled this list of things to do.

1. Install or build the ROS 2 TurtleBot 2 driver packages (such as turtlebot2_demo or ecl_turtlebot) to publish /cmd_vel, /odom, and sensor transforms (tf).
2. Ensure your LiDAR or depth sensor is active and publishing sensor_msgs/LaserScan or pointclouds.
3. 

## Testing 

### Camera

Created the `astra_camera.launch.py` file and tested the ORBBEC Astra camera.  Uses lots of CPU, about 110% to do the depth and colour camera feeds.  Just using the depth halves this.  The image shown in `rqt` is interesting.  My hand has seven or eight fingers depending on where I hold my hand!

### Kobuki Base

Start the Kobuki base using:

```bash
ros2 launch turtlebot2_main turtlebot2-base.launch.py 
```






