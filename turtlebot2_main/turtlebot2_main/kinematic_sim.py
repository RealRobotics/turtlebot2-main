import math

import rclpy
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster


class Turtlebot2KinematicSim(Node):
    def __init__(self):
        super().__init__("turtlebot2_kinematic_sim")

        self.declare_parameter("wheel_radius", 0.035)
        self.declare_parameter("wheel_separation", 0.29)
        self.declare_parameter("update_rate", 50.0)
        self.declare_parameter("cmd_vel_timeout", 0.5)

        self.wheel_radius = float(self.get_parameter("wheel_radius").value)
        self.wheel_separation = float(self.get_parameter("wheel_separation").value)
        update_rate = float(self.get_parameter("update_rate").value)
        self.cmd_vel_timeout = float(self.get_parameter("cmd_vel_timeout").value)

        self.cmd_vel = Twist()
        self.last_cmd_time = self.get_clock().now()
        self.last_update_time = self.get_clock().now()
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.left_wheel_position = 0.0
        self.right_wheel_position = 0.0

        self.create_subscription(Twist, "cmd_vel", self.cmd_vel_callback, 10)
        self.odom_publisher = self.create_publisher(Odometry, "odom", 10)
        self.joint_state_publisher = self.create_publisher(JointState, "joint_states", 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.create_timer(1.0 / update_rate, self.update)

    def cmd_vel_callback(self, message):
        self.cmd_vel = message
        self.last_cmd_time = self.get_clock().now()

    def update(self):
        now = self.get_clock().now()
        dt = (now - self.last_update_time).nanoseconds * 1e-9
        self.last_update_time = now
        if dt <= 0.0 or dt > 1.0:
            return

        command_age = (now - self.last_cmd_time).nanoseconds * 1e-9
        linear_velocity = self.cmd_vel.linear.x if command_age <= self.cmd_vel_timeout else 0.0
        angular_velocity = self.cmd_vel.angular.z if command_age <= self.cmd_vel_timeout else 0.0

        left_velocity = (
            linear_velocity - angular_velocity * self.wheel_separation / 2.0
        ) / self.wheel_radius
        right_velocity = (
            linear_velocity + angular_velocity * self.wheel_separation / 2.0
        ) / self.wheel_radius

        self.x += linear_velocity * math.cos(self.yaw) * dt
        self.y += linear_velocity * math.sin(self.yaw) * dt
        self.yaw = math.atan2(
            math.sin(self.yaw + angular_velocity * dt),
            math.cos(self.yaw + angular_velocity * dt),
        )
        self.left_wheel_position += left_velocity * dt
        self.right_wheel_position += right_velocity * dt

        self.publish_joint_states(now, left_velocity, right_velocity)
        self.publish_odometry(now, linear_velocity, angular_velocity)

    def publish_joint_states(self, stamp, left_velocity, right_velocity):
        message = JointState()
        message.header.stamp = stamp.to_msg()
        message.name = ["left_wheel_joint", "right_wheel_joint"]
        message.position = [self.left_wheel_position, self.right_wheel_position]
        message.velocity = [left_velocity, right_velocity]
        self.joint_state_publisher.publish(message)

    def publish_odometry(self, stamp, linear_velocity, angular_velocity):
        odometry = Odometry()
        odometry.header.stamp = stamp.to_msg()
        odometry.header.frame_id = "odom"
        odometry.child_frame_id = "base_footprint"
        odometry.pose.pose.position.x = self.x
        odometry.pose.pose.position.y = self.y
        odometry.pose.pose.orientation.z = math.sin(self.yaw / 2.0)
        odometry.pose.pose.orientation.w = math.cos(self.yaw / 2.0)
        odometry.twist.twist.linear.x = linear_velocity
        odometry.twist.twist.angular.z = angular_velocity
        self.odom_publisher.publish(odometry)

        transform = TransformStamped()
        transform.header.stamp = stamp.to_msg()
        transform.header.frame_id = "odom"
        transform.child_frame_id = "base_footprint"
        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.rotation.z = odometry.pose.pose.orientation.z
        transform.transform.rotation.w = odometry.pose.pose.orientation.w
        self.tf_broadcaster.sendTransform(transform)


def main(args=None):
    rclpy.init(args=args)
    node = Turtlebot2KinematicSim()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
