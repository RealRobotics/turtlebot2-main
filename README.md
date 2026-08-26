# TurtleBot2 Main Repo

The top level repo for the TurtleBot2 code.  Builds the workspace and the Kobuki drivers.  Also has some basic launch files to drive the TurtleBot2.

![TurtleBot2](turtlebot_2_lg.png)

Tested using

* ROS Lyrical and Ubuntu 26.04LTS (using the docker in this repo).

## Objective

To run the Turtlebot2 using a Raspberry Pi4 or an old laptop.  The robot should then be able to map the room and navigate between two set points avoiding obstacles and replanning as required.

## Setup and building

These docs show how the two main hardware components were built.

* [Kobuki platform build notes](build_notes_kobuki.md)
* [Orbbec Astra camera](build_notes_orbbec.md)

The code was originally built on a fast workstation inside a docker image.  [Instructions here.](docker/README.md)

A laptop was intended to be used to control the TurtleBot2, so that is what I used first.  The installation notes can be found [here](pc_installation.md) that includes building the ROS Nav2 stack. 

The next job was to get the robot to run.  This process is documented [here](running_slam.md).

## Acknowledgments

© 2026, University of Leeds.

The author, A. Blight, has asserted his moral rights.
