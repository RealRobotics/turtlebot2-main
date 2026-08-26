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

from launch_ros.actions import Node
from launch import LaunchDescription

def generate_launch_description():

    astra_camera_node = Node(
        package="astra_camera",
        executable="astra_camera_node",
        output="both",
        # Copied these values from the defaults in the 
        # astra.launch.xml file.
        parameters=[{
            "camera_name": "camera",
            "enable_color": True,
            "enable_depth": True,
            "enable_point_cloud": True,
            "enable_colored_point_cloud": False,
            "enable_ir": False,
            "enable_d2c_viewer": False,
            "enable_publish_extrinsic": False,
        }],
    )

    ld = LaunchDescription()
    ld.add_action(astra_camera_node)
    return ld
