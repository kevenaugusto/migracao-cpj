from typing import Any

import cv2
import numpy
from mss.base import MSSBase
import pyautogui


class ImageMatcher:
    @staticmethod
    def find_template(template: cv2.typing.MatLike | None, screenshot: MSSBase, monitor: int = 1):
        screen = numpy.array(screenshot.grab(screenshot.monitors[monitor]))
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_value >= 0.8:
            h, w = template.shape
            return max_loc[0], max_loc[1], w, h
        return None

    @staticmethod
    def move_mouse_to(found_template: tuple[int, int, Any, Any] | None):
        if found_template is None:
            return None
        x, y, w, h = found_template
        center_x = x + w / 2
        center_y = y + h / 2
        pyautogui.moveTo(center_x, center_y)
        return center_x, center_y
