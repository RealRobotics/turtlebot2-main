import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    EmitEvent,
    RegisterEventHandler,
)
from launch.events import matches_action
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition

def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    max_laser_range = LaunchConfiguration("max_laser_range")

    # SLAM Toolbox Configuration
    # Use the standard online synchronous parameters from slam_toolbox.
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')
    slam_params_file = os.path.join(slam_toolbox_dir, 'config', 'mapper_params_online_sync.yaml')

    slam_toolbox_node = LifecycleNode(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        namespace="",
        name='slam_toolbox',
        output='screen',
        remappings=[
            ('scan', '/scan'),
            ('map', '/map'),
            ('map_metadata', '/map_metadata'),
        ],
        parameters=[
            slam_params_file,
            {
                # Overriding specific parameter tweaks for an RPi4 environment
                'use_sim_time': use_sim_time,
                'use_lifecycle_manager': False,
                'max_laser_range': ParameterValue(max_laser_range, value_type=float),
                'minimum_time_interval': 0.1,
                'minimum_travel_distance': 0.0,
                'minimum_travel_heading': 0.0,
                'throttle_scans': 1,
                'map_frame': 'map',
                'odom_frame': 'odom',
                'base_frame': 'base_footprint',
                'map_update_interval': 1.0,
                'transform_publish_period': 0.02,
                'restamp_tf': False,
                'use_map_saver': True,
                'enable_interactive_mode': False,
                'use_scan_matching': True,
                'mode': 'mapping'
            }
        ]
    )

    configure_slam_toolbox = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(slam_toolbox_node),
            transition_id=Transition.TRANSITION_CONFIGURE,
        )
    )

    activate_slam_toolbox = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=slam_toolbox_node,
            start_state='configuring',
            goal_state='inactive',
            entities=[
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=matches_action(slam_toolbox_node),
                        transition_id=Transition.TRANSITION_ACTIVATE,
                    )
                )
            ],
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulated time from the /clock topic.",
        ),
        DeclareLaunchArgument(
            "max_laser_range",
            default_value="5.0",
            description="Maximum scan range used by SLAM (Astra camera: 5.0).",
        ),
        slam_toolbox_node,
        configure_slam_toolbox,
        activate_slam_toolbox,
    ])
