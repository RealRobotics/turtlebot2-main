# Setup and Build notes for the Orbec camera

## Setup

Install ROS Lyrical desktop release.  Add the following packages:

```bash
sudo apt install ros-lyrical-diagnostics
```

Cloned the forked version of the repo into the workspace:

```bash
mkdir -p ws/src
cd ws/src
git clone git@github.com:RealRobotics/OrbbecSDK_ROS2.git
```

## Building the Orbec camera

The first problem was many warnings from the CMakeFiles about being out of date, so changed the minimum required vesion to 3.20.

```diff
-cmake_minimum_required(VERSION 3.8)
+cmake_minimum_required(VERSION 3.20)
```

Nice command for getting lots of debug out of `colcon`.

```bash
colcon build --packages-select=orbbec_camera --event-handlers=console_cohesion+ --cmake-args -DCMAKE_VERBOSE_MAKEFILE=ON --executor sequential
```

This showed lots of issues related to missing header files:

```bash
$ colcon build --packages-select=orbbec_camera --event-handlers=console_cohesion+ --cmake-args -DCMAKE_VERBOSE_MAKEFILE=ON --executor sequential
Starting >>> orbbec_camera
--- output: orbbec_camera
...
-- Found ament_cmake: 2.8.7 (/opt/ros/lyrical/share/ament_cmake/cmake)
-- Found ament_index_cpp: 1.13.3 (/opt/ros/lyrical/share/ament_index_cpp/cmake)
-- Found builtin_interfaces: 2.4.5 (/opt/ros/lyrical/share/builtin_interfaces/cmake)
-- Found rosidl_generator_c: 5.2.1 (/opt/ros/lyrical/share/rosidl_generator_c/cmake)
-- Found rosidl_generator_cpp: 5.2.1 (/opt/ros/lyrical/share/rosidl_generator_cpp/cmake)
-- Using all available rosidl_typesupport_c: rosidl_typesupport_fastrtps_c;rosidl_typesupport_introspection_c
-- Using all available rosidl_typesupport_cpp: rosidl_typesupport_fastrtps_cpp;rosidl_typesupport_introspection_cpp
-- Found cv_bridge: 4.1.0 (/opt/ros/lyrical/share/cv_bridge/cmake)
-- Found rmw_implementation_cmake: 7.10.1 (/opt/ros/lyrical/share/rmw_implementation_cmake/cmake)
-- Found rmw_fastrtps_cpp: 9.4.8 (/opt/ros/lyrical/share/rmw_fastrtps_cpp/cmake)
-- Using RMW implementation 'rmw_fastrtps_cpp' as default
-- Found camera_info_manager: 6.4.10 (/opt/ros/lyrical/share/camera_info_manager/cmake)
-- Found image_transport: 6.4.10 (/opt/ros/lyrical/share/image_transport/cmake)
-- Found image_publisher: 7.1.6 (/opt/ros/lyrical/share/image_publisher/cmake)
-- Found orbbec_camera_msgs: 1.5.21 (/home/ubuntu/ws/install/orbbec_camera_msgs/share/orbbec_camera_msgs/cmake)
-- Found std_srvs: 5.9.2 (/opt/ros/lyrical/share/std_srvs/cmake)
-- Found tf2: 0.45.7 (/opt/ros/lyrical/share/tf2/cmake)
-- Found tf2_eigen: 0.45.7 (/opt/ros/lyrical/share/tf2_eigen/cmake)
-- Found tf2_sensor_msgs: 0.45.7 (/opt/ros/lyrical/share/tf2_sensor_msgs/cmake)
-- Found diagnostic_updater: 4.4.7 (/opt/ros/lyrical/share/diagnostic_updater/cmake)
-- ORRBEC Machine : x86_64

-- ORRBEC Machine Bits : 64

-- Found ament_lint_auto: 0.20.6 (/opt/ros/lyrical/share/ament_lint_auto/cmake)
-- Configuring done (0.8s)
-- Generating done (0.0s)
-- Build files have been written to: /home/ubuntu/ws/build/orbbec_camera
Change Dir: '/home/ubuntu/ws/build/orbbec_camera'

Run Build Command(s): /usr/bin/cmake -E env VERBOSE=1 /usr/bin/gmake -f Makefile -j24 -l24
/usr/bin/cmake -S/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera -B/home/ubuntu/ws/build/orbbec_camera --check-build-system CMakeFiles/Makefile.cmake 0
/usr/bin/cmake -E cmake_progress_start /home/ubuntu/ws/build/orbbec_camera/CMakeFiles /home/ubuntu/ws/build/orbbec_camera//CMakeFiles/progress.marks
/usr/bin/gmake  -f CMakeFiles/Makefile2 all
gmake[1]: Entering directory '/home/ubuntu/ws/build/orbbec_camera'
/usr/bin/gmake  -f CMakeFiles/orbbec_camera.dir/build.make CMakeFiles/orbbec_camera.dir/depend
/usr/bin/gmake  -f CMakeFiles/frame_latency.dir/build.make CMakeFiles/frame_latency.dir/depend
gmake[2]: Entering directory '/home/ubuntu/ws/build/orbbec_camera'
cd /home/ubuntu/ws/build/orbbec_camera && /usr/bin/cmake -E cmake_depends "Unix Makefiles" /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera /home/ubuntu/ws/build/orbbec_camera /home/ubuntu/ws/build/orbbec_camera /home/ubuntu/ws/build/orbbec_camera/CMakeFiles/orbbec_camera.dir/DependInfo.cmake "--color=" orbbec_camera
gmake[2]: Entering directory '/home/ubuntu/ws/build/orbbec_camera'
cd /home/ubuntu/ws/build/orbbec_camera && /usr/bin/cmake -E cmake_depends "Unix Makefiles" /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera /home/ubuntu/ws/build/orbbec_camera /home/ubuntu/ws/build/orbbec_camera /home/ubuntu/ws/build/orbbec_camera/CMakeFiles/frame_latency.dir/DependInfo.cmake "--color=" frame_latency
gmake[2]: Leaving directory '/home/ubuntu/ws/build/orbbec_camera'
gmake[2]: Leaving directory '/home/ubuntu/ws/build/orbbec_camera'
/usr/bin/gmake  -f CMakeFiles/orbbec_camera.dir/build.make CMakeFiles/orbbec_camera.dir/build
/usr/bin/gmake  -f CMakeFiles/frame_latency.dir/build.make CMakeFiles/frame_latency.dir/build
gmake[2]: Entering directory '/home/ubuntu/ws/build/orbbec_camera'
gmake[2]: Entering directory '/home/ubuntu/ws/build/orbbec_camera'
[  3%] Building CXX object CMakeFiles/orbbec_camera.dir/src/frame_timestamp_csv_logger.cpp.o
[  7%] Building CXX object CMakeFiles/orbbec_camera.dir/src/ob_camera_node_driver.cpp.o
[ 11%] Building CXX object CMakeFiles/orbbec_camera.dir/src/ob_camera_node.cpp.o
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/frame_timestamp_csv_logger.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/frame_timestamp_csv_logger.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/frame_timestamp_csv_logger.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/frame_timestamp_csv_logger.cpp
[ 19%] Building CXX object CMakeFiles/orbbec_camera.dir/src/ros_param_backend.cpp.o
[ 19%] Building CXX object CMakeFiles/orbbec_camera.dir/src/ros_service.cpp.o
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/ob_camera_node_driver.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/ob_camera_node_driver.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/ob_camera_node_driver.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/ob_camera_node_driver.cpp
[ 23%] Building CXX object CMakeFiles/orbbec_camera.dir/src/synced_imu_publisher.cpp.o
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/ob_camera_node.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/ob_camera_node.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/ob_camera_node.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/ob_camera_node.cpp
[ 26%] Building CXX object CMakeFiles/orbbec_camera.dir/src/jpeg_decoder.cpp.o
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/ros_param_backend.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/ros_param_backend.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/ros_param_backend.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/ros_param_backend.cpp
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/ros_service.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/ros_service.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/ros_service.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/ros_service.cpp
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/synced_imu_publisher.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/synced_imu_publisher.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/synced_imu_publisher.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/synced_imu_publisher.cpp
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/jpeg_decoder.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/jpeg_decoder.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/jpeg_decoder.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/jpeg_decoder.cpp
[ 30%] Building CXX object CMakeFiles/frame_latency.dir/tools/frame_latency.cpp.o
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dframe_latency_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/ament_cmake -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/ament_index_cpp -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/Eigen3 -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/builtin_interfaces -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/cv_bridge -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/camera_info_manager -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/image_transport -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/image_publisher -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/OpenCV -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/orbbec_camera_msgs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/rclcpp -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/rclcpp_components -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/sensor_msgs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/std_msgs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/std_srvs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tf2 -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tf2_eigen -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tf2_msgs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tf2_ros -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tf2_sensor_msgs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/Threads -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/diagnostic_updater -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/diagnostic_msgs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/statistics_msgs -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/backward_ros -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/frame_latency.dir/tools/frame_latency.cpp.o -MF CMakeFiles/frame_latency.dir/tools/frame_latency.cpp.o.d -o CMakeFiles/frame_latency.dir/tools/frame_latency.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools/frame_latency.cpp
[ 34%] Building CXX object CMakeFiles/orbbec_camera.dir/src/dynamic_params.cpp.o
[ 38%] Building CXX object CMakeFiles/orbbec_camera.dir/src/image_publisher.cpp.o
[ 42%] Building CXX object CMakeFiles/orbbec_camera.dir/src/d2c_viewer.cpp.o
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/dynamic_params.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/dynamic_params.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/dynamic_params.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/dynamic_params.cpp
[ 46%] Building CXX object CMakeFiles/orbbec_camera.dir/src/utils.cpp.o
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/image_publisher.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/image_publisher.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/image_publisher.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/image_publisher.cpp
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/d2c_viewer.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/d2c_viewer.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/d2c_viewer.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/d2c_viewer.cpp
/usr/bin/c++ -DROS_PACKAGE_NAME=\"orbbec_camera\" -Dorbbec_camera_EXPORTS -I/home/ubuntu/ws/build/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/SDK/include -I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/tools -isystem /usr/include/opencv4 -isystem /usr/include/eigen3 -fPIC -O3 -O3 -DNDEBUG -std=gnu++17 -fPIC -Wall -Wextra -Werror -Wno-pedantic -Wno-array-bounds -MD -MT CMakeFiles/orbbec_camera.dir/src/utils.cpp.o -MF CMakeFiles/orbbec_camera.dir/src/utils.cpp.o.d -o CMakeFiles/orbbec_camera.dir/src/utils.cpp.o -c /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/utils.cpp
In file included from /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/frame_timestamp_csv_logger.cpp:1:
/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include/orbbec_camera/frame_timestamp_csv_logger.h:3:10: fatal error: rclcpp/rclcpp.hpp: No such file or directory
    3 | #include <rclcpp/rclcpp.hpp>
      |          ^~~~~~~~~~~~~~~~~~~
compilation terminated.
In file included from /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/ros_param_backend.cpp:17:
/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include/orbbec_camera/ros_param_backend.h:18:10: fatal error: rclcpp/rclcpp.hpp: No such file or directory
   18 | #include <rclcpp/rclcpp.hpp>
      |          ^~~~~~~~~~~~~~~~~~~
compilation terminated.
In file included from /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/image_publisher.cpp:15:
/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include/orbbec_camera/image_publisher.h:17:10: fatal error: rclcpp/rclcpp.hpp: No such file or directory
   17 | #include <rclcpp/rclcpp.hpp>
      |          ^~~~~~~~~~~~~~~~~~~
compilation terminated.
/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/d2c_viewer.cpp:22:10: fatal error: sensor_msgs/image_encodings.hpp: No such file or directory
   22 | #include <sensor_msgs/image_encodings.hpp>
      |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
In file included from /home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/src/dynamic_params.cpp:16:
/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/include/orbbec_camera/dynamic_params.h:18:10: fatal error: rclcpp/rclcpp.hpp: No such file or directory
   18 | #include <rclcpp/rclcpp.hpp>
      |          ^~~~~~~~~~~~~~~~~~~
```

This is tricky.  The include path must not be set up correctly.  Let's focus on the `#include <rclcpp/rclcpp.hpp>` error first.  Looking at the `-I` values in the output above, the ROS include paths are wrong as it is looking for this file here: `I/home/ubuntu/ws/src/OrbbecSDK_ROS2/orbbec_camera/rclcpp ` when it is actually here: `/opt/ros/lyrical/include/rclcpp/rclcpp/rclcpp.hpp`

This comes back to the similar problem as experienced in the kobuki platform, `ament_target_dependencies` being deprecated.  Started fixing this but realised the `CMakeLists.txt` file is trying to do too much.

Manually rationalised the CMakeLists.txt file and then fixed until it builds.  There are many little issues with the CMakelists.txt file that need to be resolved, but it is good enough for now.

Started the camera.  It really didn't want to work.

Found out that there was a different repo, <https://github.com/orbbec/ros2_astra_camera>, that I should have been using.  Replaced the other repo with this one and started again.

## Building ros2_astra_camera

Forked repo as <https://github.com/RealRobotics/orbbec-ros2-astra-camera>.

Fixed usual problems with old version of CMake.

Added the following libraries to the Dockerfile so that the build starts:

* libuvc-dev libusb-1.0-0-dev  libusb-1.0-doc  libuvc0  libgoogle-glog-dev

The next problem was:

```bash
--- stderr: astra_camera
CMake Error at CMakeLists.txt:123 (ament_target_dependencies):
  Unknown CMake command "ament_target_dependencies".
```
