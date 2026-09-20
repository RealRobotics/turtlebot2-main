import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # SLAM Toolbox Configuration
    # Use the standard online synchronous parameters from slam_toolbox.
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')
    slam_params_file = os.path.join(slam_toolbox_dir, 'config', 'mapper_params_online_sync.yaml')

    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params_file,
            {
                # Overriding specific parameter tweaks for an RPi4 environment
                'use_sim_time': False,
                'max_laser_range': 5.0,     # Match the Astra's constraint
                'minimum_time_interval': 0.1,
                'mode': 'mapping'
            }
        ]
    )

    ld = LaunchDescription()
    ld.add_action(slam_toolbox_node)
    return ld
