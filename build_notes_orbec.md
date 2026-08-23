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

Fixed.  Next problem is:

```bash
--- stderr: astra_camera
CMake Error at CMakeLists.txt:121 (target_link_libraries):
  Target "astra_camera" links to:

    image_publisher::image_publisher

  but the target was not found.  Possible reasons include:

    * There is a typo in the target name.
    * A find_package call is missing for an IMPORTED target.
    * An ALIAS target is missing.
```

Spent a couple of hours going round in circles with Code's AI and Gemini.  The best version is getting these errors:

```bash
colcon build --packages-select astra_camera
Starting >>> astra_camera
--- stderr: astra_camera
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/uvc_camera_driver.cpp:15:10: fatal error: cv_bridge/cv_bridge.h: No such file or directory
   15 | #include <cv_bridge/cv_bridge.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:233: CMakeFiles/astra_camera.dir/src/uvc_camera_driver.cpp.o] Error 1
gmake[2]: *** Waiting for unfinished jobs....
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/point_cloud_proc/point_cloud_xyz.cpp:37:10: fatal error: image_geometry/pinhole_camera_model.h: No such file or directory
   37 | #include <image_geometry/pinhole_camera_model.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:79: CMakeFiles/astra_camera.dir/src/point_cloud_proc/point_cloud_xyz.cpp.o] Error 1
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/point_cloud_proc/point_cloud_xyzrgb.cpp:35:10: fatal error: message_filters/subscriber.h: No such file or directory
   35 | #include <message_filters/subscriber.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:93: CMakeFiles/astra_camera.dir/src/point_cloud_proc/point_cloud_xyzrgb.cpp.o] Error 1
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ros_service.cpp:17:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/utils.h:18:10: fatal error: tf2/LinearMath/Quaternion.h: No such file or directory
   18 | #include <tf2/LinearMath/Quaternion.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:205: CMakeFiles/astra_camera.dir/src/ros_service.cpp.o] Error 1
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ob_camera_info.cpp:17:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/utils.h:18:10: fatal error: tf2/LinearMath/Quaternion.h: No such file or directory
   18 | #include <tf2/LinearMath/Quaternion.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:135: CMakeFiles/astra_camera.dir/src/ob_camera_info.cpp.o] Error 1
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ob_camera_node.cpp:13:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/ob_camera_node.h:19:10: fatal error: cv_bridge/cv_bridge.h: No such file or directory
   19 | #include <cv_bridge/cv_bridge.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:177: CMakeFiles/astra_camera.dir/src/ob_camera_node.cpp.o] Error 1
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/ob_camera_node_factory.h:22,
                 from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ob_camera_node_factory.cpp:15:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/ob_camera_node.h:19:10: fatal error: cv_bridge/cv_bridge.h: No such file or directory
   19 | #include <cv_bridge/cv_bridge.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:163: CMakeFiles/astra_camera.dir/src/ob_camera_node_factory.cpp.o] Error 1
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/utils.cpp:13:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/utils.h:18:10: fatal error: tf2/LinearMath/Quaternion.h: No such file or directory
   18 | #include <tf2/LinearMath/Quaternion.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:219: CMakeFiles/astra_camera.dir/src/utils.cpp.o] Error 1
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ros_param_backend.cpp:13:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/ros_param_backend.h:22:7: error: ‘rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType’ has not been declared
   22 |       rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType callback);
      |       ^~~~~~
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ros_param_backend.cpp:26:6: error: variable or field ‘addOnSetParametersCallback’ declared void
   26 | void ParametersBackend::addOnSetParametersCallback(
      |      ^~~~~~~~~~~~~~~~~
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ros_param_backend.cpp:27:55: error: ‘OnParametersSetCallbackType’ is not a member of ‘rclcpp::node_interfaces::NodeParametersInterface’
   27 |     rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType callback) {
      |                                                       ^~~~~~~~~~~~~~~~~~~~~~~~~~~
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/dynamic_params.h:16,
                 from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/dynamic_params.cpp:12:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/ros_param_backend.h:22:7: error: ‘rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType’ has not been declared
   22 |       rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType callback);
      |       ^~~~~~
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/dynamic_params.cpp: In constructor ‘astra_camera::Parameters::Parameters(rclcpp::Node*)’:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/dynamic_params.cpp:19:7: error: cannot convert ‘astra_camera::Parameters::Parameters(rclcpp::Node*)::<lambda(const std::vector<rclcpp::Parameter>&)>’ to ‘int’
   19 |       [this](const std::vector<rclcpp::Parameter> &parameters) {
      |       ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      |       |
      |       astra_camera::Parameters::Parameters(rclcpp::Node*)::<lambda(const std::vector<rclcpp::Parameter>&)>
   20 |         for (const auto &parameter : parameters) {
      |         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   21 |           if (param_functions_.find(parameter.get_name()) != param_functions_.end()) {
      |           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   22 |             auto functions = param_functions_[parameter.get_name()];
      |             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   23 |             if (functions.empty()) {
      |             ~~~~~~~~~~~~~~~~~~~~~~~~
   24 |               RCLCPP_WARN_STREAM(logger_, "Parameter " << parameter.get_name()
      |               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   25 |                                                        << " can not be changed in runtime.");
      |                                                        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   26 |             } else {
      |             ~~~~~~~~
   27 |               for (const auto &func : param_functions_[parameter.get_name()]) {
      |               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   28 |                 func(parameter);
      |                 ~~~~~~~~~~~~~~~~
   29 |               }
      |               ~
   30 |             }
      |             ~
   31 |           }
      |           ~
   32 |         }
      |         ~
   33 |         rcl_interfaces::msg::SetParametersResult result;
      |         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   34 |         result.successful = true;
      |         ~~~~~~~~~~~~~~~~~~~~~~~~~
   35 |         return result;
      |         ~~~~~~~~~~~~~~
   36 |       });
      |       ~
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/ros_param_backend.h:22:85: note: initializing argument 1 of ‘void astra_camera::ParametersBackend::addOnSetParametersCallback(int)’
   22 |       rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType callback);
      |       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:191: CMakeFiles/astra_camera.dir/src/ros_param_backend.cpp.o] Error 1
gmake[2]: *** [CMakeFiles/astra_camera.dir/build.make:121: CMakeFiles/astra_camera.dir/src/dynamic_params.cpp.o] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:162: CMakeFiles/astra_camera.dir/all] Error 2
gmake: *** [Makefile:146: all] Error 2
---
Failed   <<< astra_camera [7.82s, exited with code 2]

Summary: 0 packages finished [8.01s]
  1 package failed: astra_camera
  1 package had stderr output: astra_camera
```

Built with more debugging options enabled to see what paths the `CMakeLists.txt` file is setting up.

```bash
colcon build --packages-select=astra_camera --event-handlers=console_cohesion+ --cmake-args -DCMAKE_VERBOSE_MAKEFILE=ON --executor sequential
```

Reformatted the build output for one of files so I can see the include paths.

```bash
Building CXX object CMakeFiles/astra_camera.dir/src/ob_camera_node.cpp.o
/usr/bin/c++ -DDEFAULT_RMW_IMPLEMENTATION=rmw_fastrtps_cpp -DFASTCDR_DYN_LINK -DROS_PACKAGE_NAME=\"astra_camera\" -DTINYXML2_DEBUG -DTINYXML2_IMPORT -D_FILE_OFFSET_BITS=64 -Dastra_camera_EXPORTS
-I/home/ubuntu/ws/build/astra_camera/include
-I/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include
-I/usr/include/libusb-1.0
-I/opt/ros/lyrical/include
-I/home/ubuntu/ws/install/astra_camera_msgs/include/astra_camera_msgs
-I/opt/ros/lyrical/include/camera_calibration_parsers
-I/opt/ros/lyrical/include/camera_info_manager
-I/opt/ros/lyrical/include/cv_bridge
-I/opt/ros/lyrical/include/image_transport
-I/opt/ros/lyrical/include/rclcpp_components
-I/opt/ros/lyrical/include/image_publisher
-I/opt/ros/lyrical/include/pluginlib
-I/opt/ros/lyrical/include/std_srvs
-isystem /usr/include/opencv4
-isystem /opt/ros/lyrical/include/sensor_msgs
-isystem /opt/ros/lyrical/include/std_msgs
-isystem /opt/ros/lyrical/include/service_msgs
-isystem /opt/ros/lyrical/include/rosidl_runtime_c
-isystem /opt/ros/lyrical/include/rosidl_typesupport_interface
-isystem /opt/ros/lyrical/include/rcutils
-isystem /opt/ros/lyrical/include/rosidl_runtime_cpp
-isystem /opt/ros/lyrical/include/rosidl_typesupport_fastrtps_c
-isystem /opt/ros/lyrical/include/rosidl_typesupport_fastrtps_cpp
-isystem /opt/ros/lyrical/include/rosidl_typesupport_c
-isystem /opt/ros/lyrical/include/rmw
-isystem /opt/ros/lyrical/include/rosidl_typesupport_cpp
-isystem /opt/ros/lyrical/include/builtin_interfaces
-isystem /opt/ros/lyrical/include/rosidl_buffer
-isystem /opt/ros/lyrical/include/rcpputils
-isystem /opt/ros/lyrical/include/rosidl_typesupport_introspection_c
-isystem /opt/ros/lyrical/include/rosidl_typesupport_introspection_cpp
-isystem /opt/ros/lyrical/include/ament_index_cpp
-isystem /opt/ros/lyrical/include/rclcpp
-isystem /opt/ros/lyrical/include/rclcpp_lifecycle
-isystem /opt/ros/lyrical/include/rcl_interfaces
-isystem /opt/ros/lyrical/include/message_filters
-isystem /opt/ros/lyrical/include/libstatistics_collector
-isystem /opt/ros/lyrical/include/rcl
-isystem /opt/ros/lyrical/include/rcl_yaml_param_parser
-isystem /opt/ros/lyrical/include/rosgraph_msgs
-isystem /opt/ros/lyrical/include/rosidl_dynamic_typesupport
-isystem /opt/ros/lyrical/include/statistics_msgs
-isystem /opt/ros/lyrical/include/tracetools
-isystem /opt/ros/lyrical/include/class_loader
-isystem /opt/ros/lyrical/include/composition_interfaces
-isystem /opt/ros/lyrical/include/geometry_msgs
-isystem /opt/ros/lyrical/include/tf2
-isystem /opt/ros/lyrical/include/action_msgs
-isystem /opt/ros/lyrical/include/tf2_msgs
-isystem /opt/ros/lyrical/include/tf2_ros
-isystem /opt/ros/lyrical/include/rclcpp_action
-isystem /usr/include/eigen3
-isystem /opt/ros/lyrical/include/rosidl_buffer_backend
-isystem /opt/ros/lyrical/includefastcdr
-isystem /opt/ros/lyrical/include/rcl_logging_interface
-isystem /opt/ros/lyrical/include/type_description_interfaces
-isystem /opt/ros/lyrical/include/lifecycle_msgs
-isystem /opt/ros/lyrical/include/rcl_lifecycle
-isystem /opt/ros/lyrical/include/unique_identifier_msgs
-isystem /opt/ros/lyrical/include/rcl_action
-fPIC -O3 -g -fPIC -g -std=gnu++20 -fPIC -Wall -Wextra -Wpedantic -MD -MT CMakeFiles/astra_camera.dir/src/ob_camera_node.cpp.o -MF CMakeFiles/astra_camera.dir/src/ob_camera_node.cpp.o.d -o CMakeFiles/astra_camera.dir/src/ob_camera_node.cpp.o -c /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ob_camera_node.cpp
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/uvc_camera_driver.cpp:15:10: fatal error: cv_bridge/cv_bridge.h: No such file or directory
   15 | #include <cv_bridge/cv_bridge.h>
      |          ^~~~~~~~~~~~~~~~~~~~~~~
compilation terminated.
```

Full list of missing header files.

```cpp
#include <cv_bridge/cv_bridge.h>
#include <image_geometry/pinhole_camera_model.h>
#include <message_filters/subscriber.h>
#include <tf2/LinearMath/Quaternion.h>
```

Searched for the all of the above using `find` and all not found.  Checking for missing packages.  Installed the packages in the `dockerfile`.

```docker
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-image-geometry \
    ros-${ROS_DISTRO}-message-filters \
    ros-${ROS_DISTRO}-tf2 \
```

Header names have been also been changed from `.h` to `.hpp` in the packages.  Changed in the code.

Only problem remaining is:

```bash
--- stderr: astra_camera
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/point_cloud_proc/point_cloud_xyzrgb.cpp:42:10: fatal error: image_geometry/pinhole_camera_model.hpp: No such file or directory
   42 | #include <image_geometry/pinhole_camera_model.hpp>
      |          ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

No idea why as the file is present now.

```bash
find / -name "pinhole_camera_model.hpp"
/opt/ros/lyrical/include/image_geometry/image_geometry/pinhole_camera_model.hpp
```

Checking paths in build files again.

```bash
/usr/bin/c++ -DDEFAULT_RMW_IMPLEMENTATION=rmw_fastrtps_cpp -DFASTCDR_DYN_LINK -DROS_PACKAGE_NAME=\"astra_camera\" -DTINYXML2_DEBUG -DTINYXML2_IMPORT -D_FILE_OFFSET_BITS=64 -Dastra_camera_EXPORTS
-I/home/ubuntu/ws/build/astra_camera/include
-I/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include
-I/usr/include/libusb-1.0
-I/opt/ros/lyrical/include
-I/home/ubuntu/ws/install/astra_camera_msgs/include/astra_camera_msgs
-I/opt/ros/lyrical/include/camera_calibration_parsers
-I/opt/ros/lyrical/include/camera_info_manager
-I/opt/ros/lyrical/include/cv_bridge
-I/opt/ros/lyrical/include/image_transport
-I/opt/ros/lyrical/include/rclcpp_components
-I/opt/ros/lyrical/include/image_publisher
-I/opt/ros/lyrical/include/pluginlib
-I/opt/ros/lyrical/include/std_srvs
-isystem /usr/include/opencv4
-isystem /opt/ros/lyrical/include/sensor_msgs
-isystem /opt/ros/lyrical/include/std_msgs
-isystem /opt/ros/lyrical/include/service_msgs
-isystem /opt/ros/lyrical/include/rosidl_runtime_c
-isystem /opt/ros/lyrical/include/rosidl_typesupport_interface
-isystem /opt/ros/lyrical/include/rcutils
-isystem /opt/ros/lyrical/include/rosidl_runtime_cpp
-isystem /opt/ros/lyrical/include/rosidl_typesupport_fastrtps_c
-isystem /opt/ros/lyrical/include/rosidl_typesupport_fastrtps_cpp
-isystem /opt/ros/lyrical/include/rosidl_typesupport_c
-isystem /opt/ros/lyrical/include/rmw
-isystem /opt/ros/lyrical/include/rosidl_typesupport_cpp
-isystem /opt/ros/lyrical/include/builtin_interfaces
-isystem /opt/ros/lyrical/include/rosidl_buffer
-isystem /opt/ros/lyrical/include/rcpputils
-isystem /opt/ros/lyrical/include/rosidl_typesupport_introspection_c
-isystem /opt/ros/lyrical/include/rosidl_typesupport_introspection_cpp
-isystem /opt/ros/lyrical/include/ament_index_cpp
-isystem /opt/ros/lyrical/include/rclcpp
-isystem /opt/ros/lyrical/include/rclcpp_lifecycle
-isystem /opt/ros/lyrical/include/rcl_interfaces
-isystem /opt/ros/lyrical/include/message_filters
-isystem /opt/ros/lyrical/include/libstatistics_collector
-isystem /opt/ros/lyrical/include/rcl
-isystem /opt/ros/lyrical/include/rcl_yaml_param_parser
-isystem /opt/ros/lyrical/include/rosgraph_msgs
-isystem /opt/ros/lyrical/include/rosidl_dynamic_typesupport
-isystem /opt/ros/lyrical/include/statistics_msgs
-isystem /opt/ros/lyrical/include/tracetools
-isystem /opt/ros/lyrical/include/class_loader
-isystem /opt/ros/lyrical/include/composition_interfaces
-isystem /opt/ros/lyrical/include/geometry_msgs
-isystem /opt/ros/lyrical/include/tf2
-isystem /opt/ros/lyrical/include/action_msgs
-isystem /opt/ros/lyrical/include/tf2_msgs
-isystem /opt/ros/lyrical/include/tf2_ros
-isystem /opt/ros/lyrical/include/rclcpp_action
-isystem /usr/include/eigen3
-isystem /opt/ros/lyrical/include/rosidl_buffer_backend
-isystem /opt/ros/lyrical/includefastcdr
-isystem /opt/ros/lyrical/include/rcl_logging_interface
-isystem /opt/ros/lyrical/include/type_description_interfaces
-isystem /opt/ros/lyrical/include/lifecycle_msgs
-isystem /opt/ros/lyrical/include/rcl_lifecycle
-isystem /opt/ros/lyrical/include/unique_identifier_msgs
-isystem /opt/ros/lyrical/include/rcl_action -fPIC -O3 -g -fPIC -g -std=gnu++20 -fPIC -Wall -Wextra -Wpedantic -MD -MT CMakeFiles/astra_camera.dir/src/point_cloud_proc/point_cloud_xyzrgb.cpp.o -MF CMakeFiles/astra_camera.dir/src/point_cloud_proc/point_cloud_xyzrgb.cpp.o.d -o CMakeFiles/astra_camera.dir/src/point_cloud_proc/point_cloud_xyzrgb.cpp.o -c /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/point_cloud_proc/point_cloud_xyzrgb.cpp
```

Interesting.  The `image_geomtetry` package is missing from the list of includes.  The `cv_bridge` includes are present but only in the `-I` includes whereas most other ROS include paths are in the `isystem` section.  Let's see how to fix this in the `CMakeLists.txt` file.  Added a new line in this section:

```CMake
# 5. Traditional Global Variable Header Mapping
# This uses the massive collective include array generated by the packages automatically
foreach(target ${all_targets})
  target_include_directories(${target} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    ${OpenCV_INCLUDE_DIRS}
    ${LIBUVC_INCLUDE_DIRS}
    ${GLOG_INCLUDE_DIRS}
    ${ament_cmake_INCLUDE_DIRS}  # <-- Crucial global macro collectors
    /opt/ros/lyrical/include     # <-- Permanent absolute hard link fallback
    /opt/ros/lyrical/include/image_geometry # Hack to fix missing include path.  <<< THIS LINE ADDED.
  )
```

Now that all the header files are present, we can sort out the compiler issues. There are several pages of these, so I'm going to pick the first one and fix that and repeat until done.

Problem 1

```bash
In file included from /home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/src/ros_param_backend.cpp:13:
/home/ubuntu/ws/src/orbbec-ros2-astra-camera/astra_camera/include/astra_camera/ros_param_backend.h:22:7: error: ‘rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType’ has not been declared
   22 |       rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType callback);
      |       ^~~~~~
```

The fix for this and some related fixes was all that was needed to get the code to build again.  The `CMakeLists.txt` file was also reworked to reduce the time taken for the linking phase of the build.

After this the node started properly but could not find the camera.  A change to the `docker/start.bash` fiel fix this.

Now we need to get `rviz2` to work in the docker.

Changed to use Wayland changes from ros-docker-scripts.  Much neater.  `RQt` starts OK but does not get any topics. `RViz2` fails to start, so more work to be done.  Tested with the following command:

```bash
 ros2 run image_tools showimage --remap /image:=/camera/color/image_raw
```

And it shows a lovely image of my hands and keyboard!  It works.  `RQt` and `RViz2` are separate problems.
