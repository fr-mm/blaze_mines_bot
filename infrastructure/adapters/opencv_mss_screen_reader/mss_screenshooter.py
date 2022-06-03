import os
import time
from typing import Dict

import mss
import mss.tools
from mss.base import MSSBase

from domain.entities import Image
from domain.value_objects import ImagePath, ScreenRegion, ImageName


class MssScreenshooter:
    __SCREENSHOT_FILE_NAME = 'screenshot.jpg'
    __mss: MSSBase
    __path: str

    def __init__(self) -> None:
        self.__mss = mss.mss()
        self.__path = MssScreenshooter.get_path()

    def take_full_screenshot(self) -> Image:
        self.__mss.shot(output=self.__path)
        return Image(
            name=ImageName('screenshot'),
            path=ImagePath(self.__SCREENSHOT_FILE_NAME),
            location=ScreenRegion.full_screen()
        )

    def take_screenshot_from_region(self, screen_region: ScreenRegion) -> Image:
        mss_coordinates = self.__screen_region_to_mss_coordinates(screen_region)
        screenshot = self.__mss.grab(mss_coordinates)
        mss.tools.to_png(screenshot.rgb, size=screenshot.size, output=self.__path)
        return Image(
            name=ImageName('screenshot'),
            path=ImagePath(self.__SCREENSHOT_FILE_NAME),
            location=screen_region
        )

    @staticmethod
    def get_path() -> str:
        static_directory = ImagePath.get_static_directory_path()
        return os.path.join(static_directory, MssScreenshooter.__SCREENSHOT_FILE_NAME)

    @staticmethod
    def __screen_region_to_mss_coordinates(screen_region: ScreenRegion) -> Dict[str, int]:
        return {
            'top': screen_region.top_left.y,
            'left': screen_region.top_left.x,
            'width': screen_region.bottom_right.x - screen_region.top_left.x,
            'height': screen_region.bottom_right.y - screen_region.top_left.y
        }


if __name__ == '__main__':
    time.sleep(1)
    MssScreenshooter().take_full_screenshot()
