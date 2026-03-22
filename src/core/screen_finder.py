from typing import Optional, Tuple
import autopy

Point = Tuple[float, float]


def find_image_center(image_path: str, tolerance: float = 0.05) -> Optional[Point]:
    screen = autopy.bitmap.capture_screen()
    template = autopy.bitmap.Bitmap.open(image_path)
    result = screen.find_bitmap(template, tolerance=tolerance)
    if result is None:
        return None
    x, y = result
    center_x = x + template.width / 2
    center_y = y + template.height / 2
    return center_x, center_y
