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

    # Astra Camera Configuration
    astra_camera_node = Node(
        package="astra_camera",
        executable="astra_camera_node",
        output="both",
        # Copied these values from the defaults in the
        # astra.launch.xml file.
        # There are many others, but those defaults work well enough.
        parameters=[{
            "camera_name": "camera",
            "enable_color": False,
            "enable_depth": True,
            "enable_point_cloud": True,
            "enable_colored_point_cloud": False,
            "enable_ir": False,
            "enable_d2c_viewer": False,
            "enable_publish_extrinsic": False,
        }],
    )

    # Use a minimal URDF to define the transform between the base_footprint
    # and the camera_link frames.
    # This is necessary for the depthimage_to_laserscan node to work correctly.
    robot_description_xml = """<?xml version="1.0"?>
        <robot name="turtlebot2_astra">
            <!-- Material definitions for RViz2 coloring -->
            <material name="dark_grey"><color rgba="0.2 0.2 0.2 1.0"/></material>
            <material name="black"><color rgba="0.05 0.05 0.05 1.0"/></material>

            <!-- 1. The ground-level frame published by the Kobuki driver -->
            <link name="base_footprint" />

            <!-- 2. The main physical chassis link -->
            <link name="base_link">
                <visual>
                    <!-- Offset the visual slightly so it floats correctly above the floor -->
                    <origin xyz="0.0 0.0 0.0" rpy="0.0 0.0 0.0"/>
                    <geometry>
                        <!-- Kobuki physical dimensions: ~35cm diameter, ~9cm thick -->
                        <cylinder radius="0.177" length="0.09"/>
                    </geometry>
                    <material name="dark_grey"/>
                </visual>
            </link>

            <!-- 3. The Astra Camera frame -->
            <link name="camera_link">
                <visual>
                    <origin xyz="0.0 0.0 0.0" rpy="0.0 0.0 0.0"/>
                    <geometry>
                        <!-- Rough physical envelope of the Astra camera -->
                        <box size="0.04 0.165 0.04"/>
                    </geometry>
                    <material name="black"/>
                </visual>
            </link>

            <!-- Joint linking floor to chassis (Kobuki chassis sits 2cm above the ground) -->
            <joint name="footprint_to_base_joint" type="fixed">
                <parent link="base_footprint" />
                <child link="base_link" />
                <origin xyz="0.0 0.0 0.02" rpy="0.0 0.0 0.0" />
            </joint>

            <!-- Joint linking chassis to camera (Measuring upwards from the base link)
                xyz = meters forward (x), left (y), and upward (z) from the base_link center -->
            <joint name="base_to_camera_joint" type="fixed">
                <parent link="base_link" />
                <child link="camera_link" />
                <origin xyz="0.16 0.0 0.17" rpy="0.0 0.0 0.0" />
            </joint>
        </robot>
        """

    # Publish the robot description to the ROS system so that other nodes can use it.
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_xml,
            'use_sim_time': False
        }]
    )

    # Depth Image to LaserScan Configuration
    #
    # This node takes the Astra's raw depth image and creates a 2D slice.
    # Note: If your camera topics are different, remap them below.
    depthimage_to_laserscan_node = Node(
        package='depthimage_to_laserscan',
        executable='depthimage_to_laserscan_node',
        name='depthimage_to_laserscan',
        remappings=[
            ('depth', '/depth/image_raw'),
            ('depth_camera_info', '/depth/camera_info'),
            ('scan', '/scan')
        ],
        parameters=[{
            'scan_time': 0.033,          # Match camera frame rate (~30 FPS)
            'range_min': 0.6,            # Orbbec Astra min range (meters)
            'range_max': 5.0,            # Orbbec Astra max reliable range
            'scan_height': 5,            # Number of pixel rows to sample vertically
            'output_frame': 'camera_link' # Must match your camera's TF link
        }],
        output='screen'
    )

    ld = LaunchDescription()
    ld.add_action(kobuki_ros_node)
    ld.add_action(astra_camera_node)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(depthimage_to_laserscan_node)
    return ld
