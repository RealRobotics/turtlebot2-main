import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    nav2_bringup_share = get_package_share_directory("nav2_bringup")
    turtlebot2_share = get_package_share_directory("turtlebot2_main")

    nav2_launch_file = os.path.join(
        nav2_bringup_share,
        "launch",
        "navigation_launch.py",
    )
    nav2_params_file = os.path.join(
        turtlebot2_share,
        "config",
        "nav2_params.yaml",
    )

    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_launch_file),
        launch_arguments={
            "params_file": nav2_params_file,
            "autostart": "true",
        }.items(),
    )

    return LaunchDescription([navigation])