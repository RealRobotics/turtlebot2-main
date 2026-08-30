# To Do List

## Main to do list

* Test Astra camera.  Done.
* Test Kobuki base. Done.
* Get Kobuki base driving around the floor using keyboard tele-op.
  * Not working - Fixed.
* Run SLAM.
  * Break this down into smaller tasks? Steps 1 to 15 in slam doc.
    1. Done
    2. In progress.
    3. .
    4. .
    5. .
    6. .
    7. .
    8. .
    9. .
    10. .
    11. .
    12. .
    13. .
    14. .
    15. .

## ROS things to fix

* Nav2
  * No `ros-lyrical-navigate2` package.
  * No `ros-lyrical-nav2-bringup` package.
* RQt really sucks on the old laptop.  Uses 110% CPU  (from 400%) and barely responds.

## Kobuki

* Fixed. keyop does not have launch file. ROS2 does not allow keyboard input to be caught by the nodes started in a launch file. Fixed published topics to match those used by the rest of the ROS interface.
