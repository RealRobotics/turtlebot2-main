import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    package_share = get_package_share_directory("turtlebot2_main")

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_share, "launch", "gazebo_sim.launch.py")
        ),
        launch_arguments={"rviz": LaunchConfiguration("rviz")}.items(),
    )

    # Start SLAM only after the robot has spawned and /clock and TF are flowing.
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_share, "launch", "slam_toolbox.launch.py")
        ),
        launch_arguments={
            "use_sim_time": "true",
            "max_laser_range": "12.0",
        }.items(),
    )
    delayed_slam = TimerAction(period=12.0, actions=[slam_toolbox])

    return LaunchDescription(
        [
            DeclareLaunchArgument("rviz", default_value="true"),
            gazebo,
            delayed_slam,
        ]
    )
