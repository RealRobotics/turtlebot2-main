# TurtleBot2 Main Repo

The top level repo for the TurtleBot2 code.  Builds the workspace and the Kobuki drivers.  Also has some basic launch files to drive the TurtleBot2.

![TurtleBot2](turtlebot_2_lg.png)

Tested using ROS Jazzy Jalico and Ubuntu Noble Number (24.04LTS).

## Setup and building

You need ROS Jazzy installed natively on your compupter.  Alternatively, you can use the Jazzy [Docker scripts](https://github.com/RealRobotics/ros-docker-scripts/tree/jazzy).

To setup the workspace and do the first build, open the [vars.bash][scripts/vars.bash] and change this line:

```bash
WORKSPACE_DIR=${HOME}/ws
```

to point at the place you like, e.g. I have many workspaces, so use something like this:

```bash
WORKSPACE_DIR=${HOME}/workspaces/my_cool_ws
```

Save and exit.

**Getting the workspace directory right is very important when using the Jazzy docker scripts.**

Then run the following script:

```bash
cd scripts/workspace
./setup_ws.bash
```

Note: This will clone all the repos and then build the code.

Subsequent builds can be done using `colcon build`.

## Running the code

TODO

## Documents

* [Workspace set up](setup.md)
* [Build instructions](build.md)
* [Running the TurtleBot2](running.md)
* [Notes on building the code](build_notes.md)

## Acknowledgments

© 2026, University of Leeds.

The author, A. Blight, has asserted his moral rights.
