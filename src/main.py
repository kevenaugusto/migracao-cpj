import time
from pathlib import Path

import cv2
import mss

from image_matcher import ImageMatcher

SELECTED_MONITOR = 1
PJ = cv2.imread(str(Path(__file__).parent.parent / 'assets' / 'PJ.jpeg'), 0)

def main():
    screenshot = mss.mss()
    coordenates = ImageMatcher.find_template(PJ, screenshot, SELECTED_MONITOR)
    while not coordenates:
        print("Não achou!")
        time.sleep(1)
        coordenates = ImageMatcher.find_template(PJ, screenshot, SELECTED_MONITOR)
    print("Achou!")
    ImageMatcher.move_mouse_to(coordenates)


if __name__ == '__main__':
    main()