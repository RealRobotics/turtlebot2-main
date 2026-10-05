from array import array

from turtlebot2_main.depth_scene import (
    generate_depth_image,
    obstacle_depth_from_pose,
)


def test_obstacle_range_changes_with_robot_pose():
    assert obstacle_depth_from_pose(0.0, 2.0, 5000, 300) == 2000
    assert obstacle_depth_from_pose(0.5, 2.0, 5000, 300) == 1500
    assert obstacle_depth_from_pose(2.0, 2.0, 5000, 300) == 5000


def test_depth_image_has_expected_scene_values():
    depth = generate_depth_image(
        width=8,
        height=2,
        background_depth_mm=5000,
        obstacle_depth_mm=1800,
        obstacle_center_x=4,
        obstacle_width=2,
        invalid_border=1,
    )

    assert isinstance(depth, array)
    assert depth.typecode == "H"
    assert len(depth) == 16
    assert list(depth[:8]) == [0, 5000, 5000, 1800, 1800, 5000, 5000, 0]
    assert list(depth[8:]) == [0, 5000, 5000, 1800, 1800, 5000, 5000, 0]