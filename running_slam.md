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

!!!!HERE!!!

### SLAM

To do.




