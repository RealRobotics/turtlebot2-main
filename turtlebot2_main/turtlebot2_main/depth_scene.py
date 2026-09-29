from array import array


def generate_depth_image(
    width,
    height,
    background_depth_mm,
    obstacle_depth_mm,
    obstacle_center_x,
    obstacle_width,
    invalid_border,
):
    """Create a deterministic depth image for the virtual camera scene."""
    pixels = array("H", [background_depth_mm]) * (width * height)
    obstacle_start = max(0, obstacle_center_x - obstacle_width // 2)
    obstacle_end = min(width, obstacle_start + obstacle_width)

    for row in range(height):
        row_start = row * width
        for column in range(obstacle_start, obstacle_end):
            pixels[row_start + column] = obstacle_depth_mm

        for column in range(min(invalid_border, width)):
            pixels[row_start + column] = 0
            pixels[row_start + width - column - 1] = 0

    return pixels