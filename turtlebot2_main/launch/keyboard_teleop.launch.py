from launch import LaunchDescription
from launch.actions import ExecuteProcess


def generate_launch_description():
    keyboard_teleop_process = ExecuteProcess(
        cmd=[
            "script",
            "-qec",
            "ros2 run kobuki_keyop kobuki_keyop_node",
            "/dev/null",
        ],
        output="screen",
        emulate_tty=True,
    )

    return LaunchDescription([keyboard_teleop_process])
