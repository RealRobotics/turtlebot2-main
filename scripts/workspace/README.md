# Workspace setup

This document explains how to create the ROS2 workspace needed to build and run the TankBot software.  It assumes that you using Ubuntu 24.04LTS and that you have run all the ROS2 setup scripts.

To setup and do the first build, run the following

```bash
cd ~/ws/src/pipebot_4wd/setup/workspace
./setup_ws.bash
```

Note: This build will take several minutes.

Subsequent builds can be done using `colcon build`.

## TO DO

* Test and fix `release*.bash` files.
