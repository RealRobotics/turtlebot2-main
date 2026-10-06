import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    package_share = get_package_share_directory("turtlebot2_main")
    nav2_bringup_share = get_package_share_directory("nav2_bringup")

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_share, "launch", "gazebo_sim.launch.py")
        ),
        launch_arguments={
            "x": LaunchConfiguration("x"),
            "y": LaunchConfiguration("y"),
            "rviz": LaunchConfiguration("rviz"),
        }.items(),
    )

    # Localization, planner, controller and behaviors, all activated by the
    # bringup lifecycle manager.
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_share, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "slam": "False",
            "map": LaunchConfiguration("map"),
            "params_file": os.path.join(
                package_share, "config", "nav2_params.yaml"
            ),
            "use_sim_time": "true",
            "autostart": "true",
        }.items(),
    )

    # The robot spawn pose is known in simulation, so give AMCL its initial pose.
    initial_pose = TimerAction(
        period=15.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    "ros2", "topic", "pub", "--once", "-w", "1",
                    "--qos-reliability", "reliable",
                    "/initialpose", "geometry_msgs/msg/PoseWithCovarianceStamped",
                    [
                        "{header: {frame_id: map}, pose: {pose: {position: {x: ",
                        LaunchConfiguration("x"),
                        ", y: ",
                        LaunchConfiguration("y"),
                        "}, orientation: {z: 0.0, w: 1.0}}}}",
                    ],
                ],
                output="screen",
            )
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "map",
                default_value=os.path.expanduser("~/ws/maps/turtlebot2_gz.yaml"),
                description="Map YAML saved from the Gazebo SLAM run.",
            ),
            DeclareLaunchArgument("x", default_value="-3.0"),
            DeclareLaunchArgument("y", default_value="0.0"),
            DeclareLaunchArgument("rviz", default_value="true"),
            gazebo,
            nav2,
            initial_pose,
        ]
    )
