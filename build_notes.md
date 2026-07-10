# Setup and Build notes

## Setup

Install ROS Jazzy desktop release.  Add the following packages:

```bash
sudo apt install ros-jazzy-diagnostics
```

Did this:

```bash
mkdir -p kobuki_ws/src
cd kobuki_ws/src
git clone https://github.com/kobuki-base/kobuki_ros.git
git clone https://github.com/kobuki-base/kobuki_core.git
git clone https://github.com/kobuki-base/kobuki_ros_interfaces.git
git clone https://github.com/stonier/ecl_core.git
git clone https://github.com/stonier/ecl_tools.git
```

Later, I forked all the repos as some needed fixing.  The `setup.bash` script now documents and implements this process.

## Build Notes

Started with the obvious

```bash
cd kobuki_ws
colcon build
```

### Build notes

This failed badly, so focused on one bit at a time.  These build OK.

```bash
# kobuki_ros_interfaces
colcon build --packages-select kobuki_ros_interfaces
```

These still need work.

```bash
# kobuki_ros
colcon build --packages-select kobuki_node
Starting >>> kobuki_node
[0.314s] ERROR:colcon.colcon_cmake.task.cmake.build:Failed to find the following files:
- /home/andy/workspaces/kobuki_ws/install/kobuki_core/share/kobuki_core/package.sh
Check that the following packages have been built:
- kobuki_core
Failed   <<< kobuki_node [0.00s, exited with code 1]

Summary: 0 packages finished [0.18s]
  1 package failed: kobuki_node
```

As it says, it needs `kobuki_core` to be built first, so doing that.

```bash
# kobuki_core
colcon build --packages-select kobuki_core
Starting >>> kobuki_core
--- stderr: kobuki_core
CMake Deprecation Warning at /opt/ros/kilted/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /opt/ros/kilted/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:18 (find_package)


CMake Error at CMakeLists.txt:23 (find_package):
  By not providing "Findecl_devices.cmake" in CMAKE_MODULE_PATH this project
  has asked CMake to find a package configuration file provided by
  "ecl_devices", but CMake did not find one.

  Could not find a package configuration file provided by "ecl_devices" with
  any of the following names:

    ecl_devicesConfig.cmake
    ecl_devices-config.cmake

  Add the installation prefix of "ecl_devices" to CMAKE_PREFIX_PATH or set
  "ecl_devices_DIR" to a directory containing one of the above files.  If
  "ecl_devices" provides a separate development package or SDK, be sure it
  has been installed.


---
Failed   <<< kobuki_core [0.55s, exited with code 1]

Summary: 0 packages finished [0.72s]
  1 package failed: kobuki_core
  1 package had stderr output: kobuki_core
```

Bloody ECL again!  Decided to build from scratch.

```bash
git clone https://github.com/stonier/ecl_core.git
git clone https://github.com/stonier/ecl_tools.git
```

Cloned the ECL repo and started to build that.

```bash
cd kobuki_ws/src
git clone https://github.com/stonier/ecl_core.git
cd ..
colcon build
colcon build
Starting >>> ecl_mpl
Starting >>> ecl_exceptions
Starting >>> ecl_eigen
Starting >>> kobuki_ros_interfaces
Starting >>> ecl_command_line
Starting >>> ecl_core
Starting >>> ecl_filesystem
Starting >>> kobuki_description
Starting >>> kobuki_ros
Finished <<< kobuki_ros [0.12s]
Finished <<< kobuki_description [0.13s]
Finished <<< kobuki_ros_interfaces [0.57s]
Starting >>> kobuki_bumper2pc
Starting >>> kobuki_keyop
Starting >>> kobuki_random_walker
Starting >>> kobuki_safety_controller
Finished <<< ecl_eigen [1.15s]
Finished <<< ecl_core [1.19s]
--- stderr: ecl_command_line
CMake Deprecation Warning at /opt/ros/kilted/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /opt/ros/kilted/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:13 (find_package)


---
Finished <<< ecl_command_line [2.16s]
--- stderr: ecl_exceptions
CMake Deprecation Warning at /opt/ros/kilted/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /opt/ros/kilted/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_exceptions [2.49s]
Starting >>> ecl_time
--- stderr: ecl_time
CMake Deprecation Warning at /opt/ros/kilted/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /opt/ros/kilted/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


CMake Error at CMakeLists.txt:21 (find_package):
  By not providing "Findecl_time_lite.cmake" in CMAKE_MODULE_PATH this
  project has asked CMake to find a package configuration file provided by
  "ecl_time_lite", but CMake did not find one.

  Could not find a package configuration file provided by "ecl_time_lite"
  with any of the following names:

    ecl_time_liteConfig.cmake
    ecl_time_lite-config.cmake

  Add the installation prefix of "ecl_time_lite" to CMAKE_PREFIX_PATH or set
  "ecl_time_lite_DIR" to a directory containing one of the above files.  If
  "ecl_time_lite" provides a separate development package or SDK, be sure it
  has been installed.


---
Failed   <<< ecl_time [1.21s, exited with code 1]
Aborted  <<< ecl_mpl [6.82s]
Aborted  <<< ecl_filesystem [9.70s]
Aborted  <<< kobuki_keyop [12.8s]
Aborted  <<< kobuki_bumper2pc [15.6s]
Aborted  <<< kobuki_safety_controller [20.3s]
Aborted  <<< kobuki_random_walker [28.3s]

Summary: 7 packages finished [29.1s]
  1 package failed: ecl_time
  6 packages aborted: ecl_filesystem ecl_mpl kobuki_bumper2pc kobuki_keyop kobuki_random_walker kobuki_safety_controller
  9 packages had stderr output: ecl_command_line ecl_exceptions ecl_filesystem ecl_mpl ecl_time kobuki_bumper2pc kobuki_keyop kobuki_random_walker kobuki_safety_controller
  21 packages not processed
```

ECL Tools messing so added that and built it.

```bash
cd src
git clone https://github.com/stonier/ecl_tools.git
cd -
colcon build --packages-select ecl_tools
colcon build --packages-select ecl_build
```

The next problem was:

```bash
cd src
git clone https://github.com/stonier/ecl_lite.git
cd -
colcon build --packages-select ecl_config
```

Then built everything again to find the next issue.

```bash
 colcon build
Starting >>> ecl_build
Starting >>> ecl_eigen
Starting >>> kobuki_ros_interfaces
Starting >>> ecl_core
Starting >>> ecl_license
Starting >>> ecl_lite
Starting >>> ecl_tools
Starting >>> kobuki_description
Starting >>> kobuki_ros
Finished <<< ecl_build [0.08s]
Finished <<< ecl_license [0.08s]
Finished <<< kobuki_description [0.08s]
Starting >>> ecl_config
Starting >>> ecl_mpl
Starting >>> ecl_command_line
Finished <<< kobuki_ros [0.09s]
Finished <<< ecl_eigen [0.11s]
Finished <<< ecl_core [0.11s]
Finished <<< ecl_tools [0.12s]
Finished <<< ecl_config [0.12s]
Starting >>> ecl_errors
Starting >>> ecl_console
Starting >>> ecl_converters_lite
Finished <<< kobuki_ros_interfaces [0.35s]
Starting >>> kobuki_bumper2pc
Starting >>> kobuki_keyop
Starting >>> kobuki_random_walker
Starting >>> kobuki_safety_controller
Finished <<< kobuki_bumper2pc [0.06s]
--- stderr: ecl_command_line
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:13 (find_package)


---
Finished <<< ecl_command_line [0.34s]
Finished <<< kobuki_random_walker [0.09s]
--- stderr: ecl_mpl
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_mpl [0.38s]
Starting >>> ecl_type_traits
Finished <<< ecl_lite [0.61s]
--- stderr: kobuki_keyop
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:5 (find_package)


CMake Deprecation Warning at /opt/ros/kilted/share/ament_cmake_target_dependencies/cmake/ament_target_dependencies.cmake:87 (message):
  ament_target_dependencies() is deprecated.  Use target_link_libraries()
  with modern CMake targets instead.  Try replacing this call with:

    target_link_libraries(kobuki_keyop PUBLIC
      ${geometry_msgs_TARGETS}
      ${kobuki_ros_interfaces_TARGETS}
      rclcpp::rclcpp
      rclcpp_components::component
      rclcpp_components::component_manager
    )

Call Stack (most recent call first):
  CMakeLists.txt:17 (ament_target_dependencies)


---
Finished <<< kobuki_keyop [0.52s]
--- stderr: ecl_console
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_console [0.67s]
--- stderr: kobuki_safety_controller
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:5 (find_package)


CMake Deprecation Warning at /opt/ros/kilted/share/ament_cmake_target_dependencies/cmake/ament_target_dependencies.cmake:87 (message):
  ament_target_dependencies() is deprecated.  Use target_link_libraries()
  with modern CMake targets instead.  Try replacing this call with:

    target_link_libraries(kobuki_safety_controller PUBLIC
      ${geometry_msgs_TARGETS}
      ${kobuki_ros_interfaces_TARGETS}
      ${std_msgs_TARGETS}
      rclcpp::rclcpp
      rclcpp_components::component
      rclcpp_components::component_manager
    )

Call Stack (most recent call first):
  CMakeLists.txt:18 (ament_target_dependencies)


---
Finished <<< kobuki_safety_controller [0.64s]
--- stderr: ecl_errors
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_errors [1.05s]
Starting >>> ecl_exceptions
Starting >>> ecl_time_lite
Starting >>> ecl_sigslots_lite
Starting >>> ecl_filesystem
Starting >>> ecl_io
--- stderr: ecl_io
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:30 (find_package)


In file included from /home/andy/workspaces/kobuki_ws/src/ecl_lite/ecl_io/src/lib/../../include/ecl/io/sockets.hpp:28,
                 from /home/andy/workspaces/kobuki_ws/src/ecl_lite/ecl_io/src/lib/../../include/ecl/io/poll.hpp:19,
                 from /home/andy/workspaces/kobuki_ws/src/ecl_lite/ecl_io/src/lib/poll.cpp:13:
/home/andy/workspaces/kobuki_ws/install/ecl_errors/include/ecl/errors/handlers.hpp:73:22: error: ‘virtual void ecl::Error::operator=(const ecl::ErrorFlag&)’ was hidden [-Werror=overloaded-virtual=]
   73 |         virtual void operator=(const ErrorFlag &error) { error_flag = error; }
      |                      ^~~~~~~~
/home/andy/workspaces/kobuki_ws/src/ecl_lite/ecl_io/src/lib/../../include/ecl/io/sockets.hpp:68:21: note:   by ‘ecl::SocketError::operator=’
   68 | class ecl_io_PUBLIC SocketError : public Error
      |                     ^~~~~~~~~~~
cc1plus: all warnings being treated as errors
gmake[2]: *** [src/lib/CMakeFiles/ecl_io.dir/build.make:76: src/lib/CMakeFiles/ecl_io.dir/poll.cpp.o] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:237: src/lib/CMakeFiles/ecl_io.dir/all] Error 2
gmake: *** [Makefile:146: all] Error 2
---
Failed   <<< ecl_io [0.71s, exited with code 2]
Aborted  <<< ecl_sigslots_lite [0.79s]
Aborted  <<< ecl_exceptions [0.96s]
Aborted  <<< ecl_filesystem [1.08s]
Aborted  <<< ecl_time_lite [1.52s]
Aborted  <<< ecl_converters_lite [3.60s]
Aborted  <<< ecl_type_traits [3.82s]

Summary: 18 packages finished [4.47s]
  1 package failed: ecl_io
  6 packages aborted: ecl_converters_lite ecl_exceptions ecl_filesystem ecl_sigslots_lite ecl_time_lite ecl_type_traits
  13 packages had stderr output: ecl_command_line ecl_console ecl_converters_lite ecl_errors ecl_exceptions ecl_filesystem ecl_io ecl_mpl ecl_sigslots_lite ecl_time_lite ecl_type_traits kobuki_keyop kobuki_safety_controller
  21 packages not processed

```

There were a couple of instances of the hiding bug that were easily fixed.  Committed on branch `kilted`.

The next issues were:

```bash
olcon build
Starting >>> ecl_build
Starting >>> ecl_eigen
Starting >>> kobuki_ros_interfaces
Starting >>> ecl_core
Starting >>> ecl_license
Starting >>> ecl_lite
Starting >>> ecl_tools
Starting >>> kobuki_description
Starting >>> kobuki_ros
Finished <<< ecl_license [0.10s]
Finished <<< ecl_core [0.10s]
Finished <<< kobuki_description [0.10s]
Finished <<< ecl_eigen [0.11s]
Finished <<< kobuki_ros [0.10s]
Finished <<< ecl_tools [0.11s]
Finished <<< ecl_build [0.12s]
Starting >>> ecl_config
Starting >>> ecl_mpl
Starting >>> ecl_command_line
Finished <<< ecl_lite [0.12s]
Finished <<< ecl_command_line [0.07s]
Finished <<< ecl_config [0.09s]
Starting >>> ecl_errors
Starting >>> ecl_console
Starting >>> ecl_converters_lite
Finished <<< ecl_mpl [0.09s]
Starting >>> ecl_type_traits
Finished <<< ecl_console [0.05s]
Finished <<< ecl_type_traits [0.09s]
Starting >>> ecl_concepts
Starting >>> ecl_math
Finished <<< ecl_errors [0.10s]
Starting >>> ecl_exceptions
Starting >>> ecl_time_lite
Starting >>> ecl_sigslots_lite
Starting >>> ecl_filesystem
Starting >>> ecl_io
Finished <<< ecl_converters_lite [0.11s]
Finished <<< ecl_sigslots_lite [0.08s]
Finished <<< ecl_concepts [0.11s]
Starting >>> ecl_utilities
Finished <<< ecl_filesystem [0.11s]
Finished <<< ecl_math [0.12s]
Finished <<< kobuki_ros_interfaces [0.43s]
Starting >>> kobuki_bumper2pc
Starting >>> kobuki_keyop
Starting >>> kobuki_random_walker
Starting >>> kobuki_safety_controller
Finished <<< ecl_exceptions [0.13s]
Starting >>> ecl_converters
Finished <<< ecl_io [0.13s]
Finished <<< kobuki_safety_controller [0.07s]
Finished <<< kobuki_keyop [0.08s]
Finished <<< kobuki_random_walker [0.08s]
Finished <<< kobuki_bumper2pc [0.09s]
Finished <<< ecl_utilities [0.11s]
Finished <<< ecl_converters [0.09s]
Starting >>> ecl_formatters
Finished <<< ecl_time_lite [0.57s]
Starting >>> ecl_time
--- stderr: ecl_formatters
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_formatters [1.29s]
Starting >>> ecl_containers
Starting >>> ecl_linear_algebra
--- stderr: ecl_time
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_time [3.73s]
Starting >>> ecl_threads
--- stderr: ecl_containers
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_containers [4.25s]
--- stderr: ecl_threads
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


---
Finished <<< ecl_threads [3.96s]
Starting >>> ecl_devices
Starting >>> ecl_sigslots
Starting >>> ecl_ipc
--- stderr: ecl_linear_algebra
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:20 (find_package)


---
Finished <<< ecl_linear_algebra [7.29s]
Starting >>> ecl_geometry
Starting >>> ecl_statistics
--- stderr: ecl_devices
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


CMake Warning (dev) at /usr/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (Threads)
  does not match the name of the calling package (ecl_threads).  This can
  lead to problems in calling code that expects `find_package` result
  variables (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  /usr/share/cmake-3.28/Modules/FindThreads.cmake:226 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_platform_detection.cmake:225 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:4 (ecl_detect_threads)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  CMakeLists.txt:22 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

---
Finished <<< ecl_devices [4.01s]
Starting >>> ecl_streams
--- stderr: ecl_ipc
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


CMake Warning (dev) at /usr/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (Threads)
  does not match the name of the calling package (ecl_threads).  This can
  lead to problems in calling code that expects `find_package` result
  variables (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  /usr/share/cmake-3.28/Modules/FindThreads.cmake:226 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_platform_detection.cmake:225 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:4 (ecl_detect_threads)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  CMakeLists.txt:22 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

---
Finished <<< ecl_ipc [4.67s]
--- stderr: ecl_sigslots
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


CMake Warning (dev) at /usr/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (Threads)
  does not match the name of the calling package (ecl_threads).  This can
  lead to problems in calling code that expects `find_package` result
  variables (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  /usr/share/cmake-3.28/Modules/FindThreads.cmake:226 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_platform_detection.cmake:225 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:4 (ecl_detect_threads)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  CMakeLists.txt:19 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

---
Finished <<< ecl_sigslots [5.52s]
--- stderr: ecl_geometry
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:20 (find_package)


---
Finished <<< ecl_geometry [7.70s]
Starting >>> ecl_mobile_robot
Starting >>> ecl_manipulators
--- stderr: ecl_streams
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:17 (find_package)


CMake Warning (dev) at /usr/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (Threads)
  does not match the name of the calling package (ecl_threads).  This can
  lead to problems in calling code that expects `find_package` result
  variables (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  /usr/share/cmake-3.28/Modules/FindThreads.cmake:226 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_platform_detection.cmake:225 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:4 (ecl_detect_threads)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ament_cmake_export_dependencies-extras.cmake:21 (find_package)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ecl_devicesConfig.cmake:41 (include)
  CMakeLists.txt:20 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

---
Finished <<< ecl_streams [4.32s]
Starting >>> ecl_core_apps
--- stderr: ecl_manipulators
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:20 (find_package)


---
Finished <<< ecl_manipulators [6.52s]
--- stderr: ecl_mobile_robot
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:20 (find_package)


---
Finished <<< ecl_mobile_robot [6.78s]
Starting >>> kobuki_core
--- stderr: ecl_core_apps
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:20 (find_package)


CMake Warning (dev) at /usr/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (Threads)
  does not match the name of the calling package (ecl_threads).  This can
  lead to problems in calling code that expects `find_package` result
  variables (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  /usr/share/cmake-3.28/Modules/FindThreads.cmake:226 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_platform_detection.cmake:225 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:4 (ecl_detect_threads)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ament_cmake_export_dependencies-extras.cmake:21 (find_package)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ecl_devicesConfig.cmake:41 (include)
  CMakeLists.txt:26 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

---
Finished <<< ecl_core_apps [8.67s]
--- stderr: ecl_statistics
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:20 (find_package)


---
Finished <<< ecl_statistics [18.5s]
--- stderr: kobuki_core
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  CMakeLists.txt:18 (find_package)


CMake Warning (dev) at /usr/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (Threads)
  does not match the name of the calling package (ecl_threads).  This can
  lead to problems in calling code that expects `find_package` result
  variables (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  /usr/share/cmake-3.28/Modules/FindThreads.cmake:226 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_platform_detection.cmake:225 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:4 (ecl_detect_threads)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ament_cmake_export_dependencies-extras.cmake:21 (find_package)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ecl_devicesConfig.cmake:41 (include)
  CMakeLists.txt:23 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

---
Finished <<< kobuki_core [8.05s]
Starting >>> kobuki_auto_docking
Starting >>> kobuki_node
--- stderr: kobuki_auto_docking
CMake Deprecation Warning at /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/cotire.cmake:45 (cmake_minimum_required):
  Compatibility with CMake < 3.5 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.
Call Stack (most recent call first):
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_buildConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:2 (find_package)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ament_cmake_export_dependencies-extras.cmake:21 (find_package)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ecl_devicesConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/kobuki_core/share/kobuki_core/cmake/ament_cmake_export_dependencies-extras.cmake:21 (find_package)
  /home/andy/workspaces/kobuki_ws/install/kobuki_core/share/kobuki_core/cmake/kobuki_coreConfig.cmake:41 (include)
  CMakeLists.txt:16 (find_package)


CMake Warning (dev) at /usr/share/cmake-3.28/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (Threads)
  does not match the name of the calling package (ecl_threads).  This can
  lead to problems in calling code that expects `find_package` result
  variables (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  /usr/share/cmake-3.28/Modules/FindThreads.cmake:226 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
  /home/andy/workspaces/kobuki_ws/install/ecl_build/share/ecl_build/cmake/ecl_platform_detection.cmake:225 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threads-extras.cmake:4 (ecl_detect_threads)
  /home/andy/workspaces/kobuki_ws/install/ecl_threads/share/ecl_threads/cmake/ecl_threadsConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ament_cmake_export_dependencies-extras.cmake:21 (find_package)
  /home/andy/workspaces/kobuki_ws/install/ecl_devices/share/ecl_devices/cmake/ecl_devicesConfig.cmake:41 (include)
  /home/andy/workspaces/kobuki_ws/install/kobuki_core/share/kobuki_core/cmake/ament_cmake_export_dependencies-extras.cmake:21 (find_package)
  /home/andy/workspaces/kobuki_ws/install/kobuki_core/share/kobuki_core/cmake/kobuki_coreConfig.cmake:41 (include)
  CMakeLists.txt:16 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Deprecation Warning at /opt/ros/kilted/share/ament_cmake_target_dependencies/cmake/ament_target_dependencies.cmake:87 (message):
  ament_target_dependencies() is deprecated.  Use target_link_libraries()
  with modern CMake targets instead.  Try replacing this call with:

    target_link_libraries(kobuki_auto_docking PUBLIC
      ${geometry_msgs_TARGETS}
      ${kobuki_ros_interfaces_TARGETS}
      ${nav_msgs_TARGETS}
      ${rcl_interfaces_TARGETS}
      ${std_msgs_TARGETS}
      kobuki_core::kobuki_core
      message_filters::message_filters
      rclcpp::rclcpp
      rclcpp_action::rclcpp_action
      rclcpp_components::component
      rclcpp_components::component_manager
      tf2_geometry_msgs::tf2_geometry_msgs
      tf2_ros::static_transform_broadcaster_node
      tf2_ros::tf2_ros
    )

Call Stack (most recent call first):
  CMakeLists.txt:36 (ament_target_dependencies)


In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/src/auto_docking_ros.cpp:19:
/opt/ros/kilted/include/message_filters/message_filters/subscriber.h:18:2: error: #warning This header is obsolete, please include message_filters/subscriber.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/subscriber.hpp instead
      |  ^~~~~~~
In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/src/auto_docking_ros.cpp:20:
/opt/ros/kilted/include/message_filters/message_filters/synchronizer.h:18:2: error: #warning This header is obsolete, please include message_filters/synchronizer.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/synchronizer.hpp instead
      |  ^~~~~~~
In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/include/kobuki_auto_docking/auto_docking_ros.hpp:28,
                 from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/src/auto_docking_ros.cpp:33:
/opt/ros/kilted/include/message_filters/message_filters/time_synchronizer.h:18:2: error: #warning This header is obsolete, please include message_filters/time_synchronizer.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/time_synchronizer.hpp instead
      |  ^~~~~~~
In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/include/kobuki_auto_docking/auto_docking_ros.hpp:30:
/opt/ros/kilted/include/message_filters/message_filters/sync_policies/approximate_time.h:18:2: error: #warning This header is obsolete, please include message_filters/approximate_time.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/approximate_time.hpp instead
      |  ^~~~~~~
cc1plus: all warnings being treated as errors
gmake[2]: *** [CMakeFiles/kobuki_auto_docking.dir/build.make:76: CMakeFiles/kobuki_auto_docking.dir/src/auto_docking_ros.cpp.o] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:139: CMakeFiles/kobuki_auto_docking.dir/all] Error 2
gmake: *** [Makefile:146: all] Error 2
---
Failed   <<< kobuki_auto_docking [17.0s, exited with code 2]
Aborted  <<< kobuki_node [38.0s]

Summary: 44 packages finished [1min 10s]
  1 package failed: kobuki_auto_docking
  1 package aborted: kobuki_node
  17 packages had stderr output: ecl_containers ecl_core_apps ecl_devices ecl_formatters ecl_geometry ecl_ipc ecl_linear_algebra ecl_manipulators ecl_mobile_robot ecl_sigslots ecl_statistics ecl_streams ecl_threads ecl_time kobuki_auto_docking kobuki_core kobuki_node
```

Ignoring the developer warnings, we have to fix this problem next.

```bash
--- stderr: kobuki_auto_docking
In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/src/auto_docking_ros.cpp:19:
/opt/ros/kilted/include/message_filters/message_filters/subscriber.h:18:2: error: #warning This header is obsolete, please include message_filters/subscriber.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/subscriber.hpp instead
      |  ^~~~~~~
In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/src/auto_docking_ros.cpp:20:
/opt/ros/kilted/include/message_filters/message_filters/synchronizer.h:18:2: error: #warning This header is obsolete, please include message_filters/synchronizer.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/synchronizer.hpp instead
      |  ^~~~~~~
In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/include/kobuki_auto_docking/auto_docking_ros.hpp:28,
                 from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/src/auto_docking_ros.cpp:33:
/opt/ros/kilted/include/message_filters/message_filters/time_synchronizer.h:18:2: error: #warning This header is obsolete, please include message_filters/time_synchronizer.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/time_synchronizer.hpp instead
      |  ^~~~~~~
In file included from /home/andy/workspaces/kobuki_ws/src/kobuki_ros/kobuki_auto_docking/include/kobuki_auto_docking/auto_docking_ros.hpp:30:
/opt/ros/kilted/include/message_filters/message_filters/sync_policies/approximate_time.h:18:2: error: #warning This header is obsolete, please include message_filters/approximate_time.hpp instead [-Werror=cpp]
   18 | #warning This header is obsolete, please include message_filters/approximate_time.hpp instead
      |  ^~~~~~~
cc1plus: all warnings being treated as errors
gmake[2]: *** [CMakeFiles/kobuki_auto_docking.dir/build.make:76: CMakeFiles/kobuki_auto_docking.dir/src/auto_docking_ros.cpp.o] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:139: CMakeFiles/kobuki_auto_docking.dir/all] Error 2
gmake: *** [Makefile:146: all] Error 2
---
Failed   <<< kobuki_auto_docking [19.2s, exited with code 2]

Summary: 45 packages finished [20.7s]
  1 package failed: kobuki_auto_docking
  1 package had stderr output: kobuki_auto_docking
```

This is in the kobuki domain, so `ECL` and the `kobuki_core` is building OK.  We can just exclude this from the  build using:

```bash
colcon build --packages-skip kobuki_auto_docking
```

All building OK.

Time taken: 90 minutes.

Found more errors and warnings.  Had to add sophus package for ECL.

```bash
git clone https://github.com/stonier/sophus.git
git co release/1.3.x
git co -b kilted
```

This had several issues, so created new branch and used GPT to fix them.  Committed.

Fixed remaining build errors in `kobuki_node`.

Taken another 90 minutes.  Now to run it!

## Running the code
