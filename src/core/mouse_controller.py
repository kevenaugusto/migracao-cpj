from typing import Tuple
import autopy

Point = Tuple[float, float]


def move_mouse_to(point: Point) -> None:
    x, y = point
    autopy.mouse.smooth_move(x, y)
