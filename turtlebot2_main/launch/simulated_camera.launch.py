import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory("turtlebot2_main")
    use_sim_time = LaunchConfiguration("use_sim_time")

    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_share, "launch", "urdf_rviz.launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    synthetic_camera = Node(
        package="turtlebot2_main",
        executable="turtlebot2_synthetic_camera",
        name="synthetic_astra_camera",
        output="screen",
        parameters=[
            os.path.join(package_share, "config", "synthetic_camera.yaml"),
            {"use_sim_time": use_sim_time},
        ],
    )

    depthimage_to_laserscan = Node(
        package="depthimage_to_laserscan",
        executable="depthimage_to_laserscan_node",
        name="depthimage_to_laserscan",
        output="screen",
        remappings=[
            ("depth", "/depth/image_raw"),
            ("depth_camera_info", "/depth/camera_info"),
            ("scan", "/scan"),
        ],
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "scan_time": 0.033,
                "range_min": 0.6,
                "range_max": 5.0,
                "scan_height": 5,
                "output_frame": "camera_depth_frame",
            }
        ],
    )

    return LaunchDescription([robot_launch, synthetic_camera, depthimage_to_laserscan])