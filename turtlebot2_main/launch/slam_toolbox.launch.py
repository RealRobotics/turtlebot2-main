import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # ==========================================
    # 1. Depth Image to LaserScan Configuration
    # ==========================================
    # This node takes the Astra's raw depth image and creates a 2D slice.
    # Note: If your camera topics are different, remap them below.
    depthimage_to_laserscan_node = Node(
        package='depthimage_to_laserscan',
        executable='depthimage_to_laserscan_node',
        name='depthimage_to_laserscan',
        remappings=[
            ('depth', '/camera/depth/image_raw'),
            ('depth_camera_info', '/camera/depth/camera_info'),
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

    # ==========================================
    # 2. SLAM Toolbox Configuration
    # ==========================================
    # We use the standard online synchronous parameters from slam_toolbox.
    # On an RPi4, online_sync balances accuracy well without dropping vital scans.
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

    return LaunchDescription([
        depthimage_to_laserscan_node,
        slam_toolbox_node
    ])
