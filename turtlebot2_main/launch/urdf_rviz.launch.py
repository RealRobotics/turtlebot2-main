import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory("turtlebot2_main")
    urdf_path = os.path.join(package_share, "urdf", "turtlebot2_se.urdf")
    rviz_config_path = os.path.join(package_share, "config", "turtlebot2.rviz")

    with open(urdf_path, "r", encoding="utf-8") as urdf_file:
        robot_description = urdf_file.read()

    use_sim_time = LaunchConfiguration("use_sim_time")

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": use_sim_time,
            }
        ],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_path],
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )

    kinematic_sim = Node(
        package="turtlebot2_main",
        executable="turtlebot2_kinematic_sim",
        name="turtlebot2_kinematic_sim",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulated time from the /clock topic.",
            ),
            robot_state_publisher,
            kinematic_sim,
            rviz,
        ]
    )
