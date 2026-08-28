# Setup and Build notes

## Setup

Install ROS Lyrical desktop release.  Add the following packages:

```bash
sudo apt install ros-lyrical-diagnostics
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

Did a clean build and the build of `sophus` failed.  There were many errors like this:

```bash
$ colcon build --packages-select=sophus --event-handlers=console_cohesion+ --cmake-args -DCMAKE_VERBOSE_MAKEFILE=ON --executor sequential
Starting >>> sophus
--- output: sophus
Change Dir: '/home/ubuntu/ws/build/sophus'
...
[ 92%] Built target test_geometry
In file included from /usr/lib/gcc/x86_64-linux-gnu/15/include/emmintrin.h:31,
                 from /usr/include/eigen3/Eigen/src/Core/util/ConfigureVectorization.h:346,
                 from /usr/include/eigen3/Eigen/Core:22,
                 from /usr/include/eigen3/unsupported/Eigen/MatrixFunctions:17,
                 from /home/ubuntu/ws/src/sophus/test/core/test_sim2.cpp:3:
In function ‘__m128 _mm_loadu_ps(const float*)’,
    inlined from ‘Packet Eigen::internal::ploadu(const typename unpacket_traits<T>::type*) [with Packet = __vector(4) float]’ at /usr/include/eigen3/Eigen/src/Core/arch/SSE/PacketMath.h:739:22,
    inlined from ‘Packet Eigen::internal::ploadt(const typename unpacket_traits<T>::type*) [with Packet = __vector(4) float; int Alignment = 0]’ at /usr/include/eigen3/Eigen/src/Core/GenericPacketMath.h:969:26,
    inlined from ‘PacketType Eigen::internal::evaluator<Eigen::PlainObjectBase<Derived> >::packet(Eigen::Index, Eigen::Index) const [with int LoadMode = 0; PacketType = __vector(4) float; Derived = Eigen::Matrix<float, 2, 1>]’ at /usr/include/eigen3/Eigen/src/Core/CoreEvaluators.h:238:42,
    inlined from ‘void Eigen::internal::generic_dense_assignment_kernel<DstEvaluatorTypeT, SrcEvaluatorTypeT, Functor, Version>::assignPacket(Eigen::Index, Eigen::Index) [with int StoreMode = 16; int LoadMode = 0; PacketType = __vector(4) float; DstEvaluatorTypeT = Eigen::internal::evaluator<Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false> >; SrcEvaluatorTypeT = Eigen::internal::evaluator<Eigen::Matrix<float, 2, 1> >; Functor = Eigen::internal::assign_op<float, float>; int Version = 0]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:675:116,
    inlined from ‘void Eigen::internal::generic_dense_assignment_kernel<DstEvaluatorTypeT, SrcEvaluatorTypeT, Functor, Version>::assignPacketByOuterInner(Eigen::Index, Eigen::Index) [with int StoreMode = 16; int LoadMode = 0; PacketType = __vector(4) float; DstEvaluatorTypeT = Eigen::internal::evaluator<Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false> >; SrcEvaluatorTypeT = Eigen::internal::evaluator<Eigen::Matrix<float, 2, 1> >; Functor = Eigen::internal::assign_op<float, float>; int Version = 0]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:689:48,
    inlined from ‘static void Eigen::internal::dense_assignment_loop<Kernel, 4, 0>::run(Kernel&) [with Kernel = Eigen::internal::generic_dense_assignment_kernel<Eigen::internal::evaluator<Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false> >, Eigen::internal::evaluator<Eigen::Matrix<float, 2, 1> >, Eigen::internal::assign_op<float, float>, 0>]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:572:86,
    inlined from ‘void Eigen::internal::call_dense_assignment_loop(DstXprType&, const SrcXprType&, const Functor&) [with DstXprType = Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false>; SrcXprType = Eigen::Matrix<float, 2, 1>; Functor = assign_op<float, float>]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:785:37,
    inlined from ‘static void Eigen::internal::Assignment<DstXprType, SrcXprType, Functor, Eigen::internal::Dense2Dense, Weak>::run(DstXprType&, const SrcXprType&, const Functor&) [with DstXprType = Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false>; SrcXprType = Eigen::Matrix<float, 2, 1>; Functor = Eigen::internal::assign_op<float, float>; Weak = void]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:954:31,
    inlined from ‘void Eigen::internal::call_assignment_no_alias(Dst&, const Src&, const Func&) [with Dst = Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false>; Src = Eigen::Matrix<float, 2, 1>; Func = assign_op<float, float>]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:890:49,
    inlined from ‘void Eigen::internal::call_assignment(Dst&, const Src&, const Func&, typename enable_if<(! evaluator_assume_aliasing<Src>::value), void*>::type) [with Dst = Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false>; Src = Eigen::Matrix<float, 2, 1>; Func = assign_op<float, float>]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:858:27,
    inlined from ‘void Eigen::internal::call_assignment(Dst&, const Src&) [with Dst = Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false>; Src = Eigen::Matrix<float, 2, 1>]’ at /usr/include/eigen3/Eigen/src/Core/AssignEvaluator.h:836:18,
    inlined from ‘Derived& Eigen::MatrixBase<Derived>::operator=(const Eigen::DenseBase<OtherDerived>&) [with OtherDerived = Eigen::Matrix<float, 2, 1>; Derived = Eigen::Block<Eigen::Matrix<float, 4, 1>, -1, -1, false>]’ at /usr/include/eigen3/Eigen/src/Core/Assign.h:66:28,
    inlined from ‘Eigen::CommaInitializer<MatrixType>::CommaInitializer(XprType&, const Eigen::DenseBase<OtherDerived>&) [with OtherDerived = Eigen::Matrix<float, 2, 1>; XprType = Eigen::Matrix<float, 4, 1>]’ at /usr/include/eigen3/Eigen/src/Core/CommaInitializer.h:48:51,
    inlined from ‘Eigen::CommaInitializer<Derived> Eigen::DenseBase<Derived>::operator<<(const Eigen::DenseBase<OtherDerived>&) [with OtherDerived = Eigen::Matrix<float, 2, 1>; Derived = Eigen::Matrix<float, 4, 1>]’ at /usr/include/eigen3/Eigen/src/Core/CommaInitializer.h:159:72,
    inlined from ‘Sophus::Vector<typename Eigen::internal::traits<T>::Scalar, 4> Sophus::Sim2Base<Derived>::params() const [with Derived = Sophus::Sim2<float>]’ at /home/ubuntu/ws/src/sophus/sophus/sim2.hpp:278:7,
    inlined from ‘bool Sophus::LieGroupTests<LieGroup_>::testRandomSmoke() [with LieGroup_ = Sophus::Sim2<float>]’ at /home/ubuntu/ws/src/sophus/test/core/tests.hpp:523:7,
    inlined from ‘bool Sophus::LieGroupTests<LieGroup_>::doesLargeTestSetPass() [with LieGroup_ = Sophus::Sim2<float>]’ at /home/ubuntu/ws/src/sophus/test/core/tests.hpp:638:30,
    inlined from ‘Sophus::enable_if_t<((bool)std::is_floating_point<S>::value), bool> Sophus::LieGroupTests<LieGroup_>::doAllTestsPass() [with S = float; LieGroup_ = Sophus::Sim2<float>]’ at /home/ubuntu/ws/src/sophus/test/core/tests.hpp:607:32,
    inlined from ‘bool Sophus::Tests<Scalar>::testLieProperties() [with Scalar = float]’ at /home/ubuntu/ws/src/sophus/test/core/test_sim2.cpp:85:32,
    inlined from ‘void Sophus::Tests<Scalar>::runAll() [with Scalar = float]’ at /home/ubuntu/ws/src/sophus/test/core/test_sim2.cpp:76:36,
    inlined from ‘int Sophus::test_sim3()’ at /home/ubuntu/ws/src/sophus/test/core/test_sim2.cpp:216:24:
/usr/lib/gcc/x86_64-linux-gnu/15/include/xmmintrin.h:982:23: error: array subscript ‘__m128_u[0]’ is partly outside array bounds of ‘Sophus::Vector<float, 2, 0> [1]’ {aka ‘Eigen::Matrix<float, 2, 1> [1]’} [-Werror=array-bounds=]
  982 |   return *(__m128_u *)__P;
      |                       ^~~
    cc1plus: all warnings being treated as errors
```

As -werror is enabled, this warning stops the build.  Added this line to the CMakeLists.txt file so the bulid completes.

```cmake
add_definitions(-DEIGEN_DONT_ALIGN)
```

Not an ideal solution as the code should be fixed properly, but it is not my code so this will do for now.

## Testing the code

To test the Kobuki base, start using this command:

```bash
$ ros2 launch turtlebot2_main turtlebot2-base.launch.py 
```

When the Kobuki base connects to this ROS program, the base plays and ascending tune.  When disconnected, there a a short pause and then the base plays a descending tune. 

If you don't hea r the tone, then check the output for something like this:

```bash
$ ros2 launch turtlebot2_main turtlebot2-base.launch.py 
[INFO] [launch]: All log files can be found below /home/andy/.ros/log/
...
[kobuki_ros_node-1] terminate called after throwing an instance of 'ecl::StandardException'
[kobuki_ros_node-1]   what():  
[kobuki_ros_node-1] Location : /home/andy/ws/src/kobuki_core/src/driver/kobuki.cpp:147 
[kobuki_ros_node-1]          : /home/andy/ws/src/ecl_core/ecl_devices/src/lib/serial_pos.cpp:117 
[kobuki_ros_node-1] Flag     : The caller does not have the required permissions.
[kobuki_ros_node-1] Detail   : Could not open /dev/ttyUSB0. Access permission was denied.
```

To fix this, enter : 

```bash
sudo usermod -a -G dialout $USER
```

and then log out and in again so this change takes effect.

The following topics and services should start up (no actions run):

```bash
$ ros2 topic list
/commands/controller_info
/commands/digital_output
/commands/external_power
/commands/led1
/commands/led2
/commands/motor_power
/commands/reset_odometry
/commands/sound
/commands/velocity
/controller_info
/debug/raw_control_command
/debug/raw_data_command
/debug/raw_data_stream
/diagnostics
/events/bumper
/events/button
/events/cliff
/events/digital_input
/events/power_system
/events/robot_state
/events/wheel_drop
/joint_states
/odom
/parameter_events
/rosout
/sensors/battery_state
/sensors/core
/sensors/dock_ir
/sensors/imu_data
/sensors/imu_data_raw
/tf
/version_info
$ ros2 service list
/kobuki/describe_parameters
/kobuki/get_parameter_types
/kobuki/get_parameters
/kobuki/get_type_description
/kobuki/list_parameters
/kobuki/set_parameters
/kobuki/set_parameters_atomically
```

### Testing publishers

The following commands were used to check the topic publishers were working when on the desktop:

```bash
# Software version number of the Kobuki base plus other info.
ros2 topic echo /version_info
# Lots of info on this.
ros2 topic echo /diagnostics
# One message per button event (press or release)
ros2 topic echo /events/button
# One message for each of the three bumper switch state changes. 
# 0 left, 1 centre, 2 right.  
# Often more than one switch is pressed when the plastic bumper is pressed.
ros2 topic echo /events/bumper
# 3 downward facing IR range sensors on the front.
# 0 left, 1 centre, 2 right.  
# Returns sensor number, state (0 no cliff, 1 cliff) and distance in mm.
ros2 topic echo /events/cliff
ros2 topic echo /sensors/imu_data
ros2 topic echo /odom
# This works nicely, 15.3V = 65%.  
ros2 topic echo /sensors/battery_state
#  Has most of what you actually need to run this base.
ros2 topic echo /sensors/core 
# I don't have one of these so always 0 values.
ros2 topic echo /sensors/dock_ir  
# Seems about right. 
ros2 topic echo /joint_states
```

Commands tested were:

```bash
# 0 off, 1 green, 2 orange, 3 red.
ros2 topic pub -1 /commands/led1 kobuki_ros_interfaces/msg/Led "{'value':1}"
ros2 topic pub -1 /commands/led2 kobuki_ros_interfaces/msg/Led "{'value':3}"
# Many different sounds, 0 - 6.
ros2 topic pub -1 /commands/sound kobuki_ros_interfaces/msg/Sound "{'value':2}"
```

Got bored with testing at this point.  Everything works so far, so fix any bugs if I find them. 

