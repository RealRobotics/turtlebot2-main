# To Do List

## Main to do list

* Test Astra camera.  Done.
* Test Kobuki base. Done.
* Get Kobuki base driving around the floor using keyboard tele-op. 
    * Not working - see below.
* Run SLAM. 
    * Break this down into smaller tasks?


## ROS things to fix

* Nav2 
    * No `ros-lyrical-navigate2` package.
    * No `ros-lyrical-nav2-bringup` package.
* RQt really sucks on the old laptop.  Uses 110% CPU  (from 400%) and barely responds.

## Kobuki

* keyop does not have launch file.  Should be able to launch using ROS 1 command `roslaunch kobuki_keyop robot_core.launch` but there is no launch file for this ROS2 branch. 
    * Added launch file. The code it uses doesn't work. 

