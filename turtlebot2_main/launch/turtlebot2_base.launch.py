# MIT License
#
# Copyright (c) 2026 University of Leeds
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ament_index_python.packages
from launch import LaunchDescription
from launch_ros.actions import Node
import os
import yaml


def generate_launch_description():

    # Command line for the main node
    #  ros2 launch kobuki_node kobuki_node-launch.py
    # The stuff below is taken from the kobuki_node-launch.py file.

    share_dir = ament_index_python.packages.get_package_share_directory("kobuki_node")

    # There are two different ways to pass parameters to a non-composed node;
    # either by specifying the path to the file containing the parameters, or by
    # passing a dictionary containing the key -> value pairs of the parameters.
    # When starting a *composed* node on the other hand, only the dictionary
    # style is supported.  To keep the code between the non-composed and
    # composed launch file similar, we use that style here as well.
    params_file = os.path.join(share_dir, "config", "kobuki_node_params.yaml")
    with open(params_file, "r") as f:
        params = yaml.safe_load(f)["kobuki_ros_node"]["ros__parameters"]

    kobuki_ros_node = Node(
        package="kobuki_node",
        executable="kobuki_ros_node",
        output="both",
        parameters=[params],
    )

    ld = LaunchDescription()
    ld.add_action(kobuki_ros_node)
    return ld
