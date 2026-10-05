import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image

from turtlebot2_main.depth_scene import (
    generate_depth_image,
    obstacle_depth_from_pose,
)


class SyntheticAstraCamera(Node):
    def __init__(self):
        super().__init__("synthetic_astra_camera")

        self.declare_parameter("width", 640)
        self.declare_parameter("height", 480)
        self.declare_parameter("frame_rate", 30.0)
        self.declare_parameter("frame_id", "camera_depth_optical_frame")
        self.declare_parameter("focal_length_x", 570.0)
        self.declare_parameter("focal_length_y", 570.0)
        self.declare_parameter("principal_point_x", 319.5)
        self.declare_parameter("principal_point_y", 239.5)
        self.declare_parameter("background_depth_mm", 3000)
        self.declare_parameter("obstacle_world_x", 2.0)
        self.declare_parameter("minimum_obstacle_distance_mm", 300)
        self.declare_parameter("obstacle_center_x", 320)
        self.declare_parameter("obstacle_width", 160)
        self.declare_parameter("invalid_border", 4)

        self.width = int(self.get_parameter("width").value)
        self.height = int(self.get_parameter("height").value)
        self.frame_id = str(self.get_parameter("frame_id").value)
        self.frame_rate = float(self.get_parameter("frame_rate").value)
        self.focal_length_x = float(self.get_parameter("focal_length_x").value)
        self.focal_length_y = float(self.get_parameter("focal_length_y").value)
        self.principal_point_x = float(
            self.get_parameter("principal_point_x").value
        )
        self.principal_point_y = float(
            self.get_parameter("principal_point_y").value
        )
        self.background_depth_mm = int(
            self.get_parameter("background_depth_mm").value
        )
        self.obstacle_world_x = float(
            self.get_parameter("obstacle_world_x").value
        )
        self.minimum_obstacle_distance_mm = int(
            self.get_parameter("minimum_obstacle_distance_mm").value
        )
        self.obstacle_center_x = int(
            self.get_parameter("obstacle_center_x").value
        )
        self.obstacle_width = int(self.get_parameter("obstacle_width").value)
        self.invalid_border = int(self.get_parameter("invalid_border").value)
        self.robot_x = 0.0

        self.create_subscription(Odometry, "odom", self.odometry_callback, 10)
        self.image_publisher = self.create_publisher(Image, "depth/image_raw", 10)
        self.camera_info_publisher = self.create_publisher(
            CameraInfo, "depth/camera_info", 10
        )
        self.create_timer(1.0 / self.frame_rate, self.publish_camera_data)

    def odometry_callback(self, message):
        self.robot_x = message.pose.pose.position.x

    def publish_camera_data(self):
        stamp = self.get_clock().now().to_msg()
        obstacle_depth_mm = obstacle_depth_from_pose(
            self.robot_x,
            self.obstacle_world_x,
            self.background_depth_mm,
            self.minimum_obstacle_distance_mm,
        )
        depth = generate_depth_image(
            self.width,
            self.height,
            self.background_depth_mm,
            obstacle_depth_mm,
            self.obstacle_center_x,
            self.obstacle_width,
            self.invalid_border,
        )

        image = Image()
        image.header.stamp = stamp
        image.header.frame_id = self.frame_id
        image.height = self.height
        image.width = self.width
        image.encoding = "16UC1"
        image.is_bigendian = 0
        image.step = self.width * 2
        image.data = depth.tobytes()
        self.image_publisher.publish(image)

        camera_info = CameraInfo()
        camera_info.header = image.header
        camera_info.height = self.height
        camera_info.width = self.width
        camera_info.distortion_model = "plumb_bob"
        camera_info.k = [
            self.focal_length_x,
            0.0,
            self.principal_point_x,
            0.0,
            self.focal_length_y,
            self.principal_point_y,
            0.0,
            0.0,
            1.0,
        ]
        camera_info.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        camera_info.p = [
            self.focal_length_x,
            0.0,
            self.principal_point_x,
            0.0,
            0.0,
            self.focal_length_y,
            self.principal_point_y,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
        ]
        self.camera_info_publisher.publish(camera_info)


def main(args=None):
    rclpy.init(args=args)
    node = SyntheticAstraCamera()
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