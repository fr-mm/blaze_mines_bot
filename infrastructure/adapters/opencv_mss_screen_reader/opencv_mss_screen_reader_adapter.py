import cv2
import mss
from mss.base import MSSBase
import mss.tools
import numpy

from domain.exceptions import ImageNotInScreenException
from domain.ports import ScreenReaderPort
from domain.value_objects import ImagePath, ScreenRegion, Coordinates


class OpencvMssScreenReaderAdapter(ScreenReaderPort):
    __SCREEN_SHOT_NAME = 'screenshot.png'
    __THRESHOLD = 0.85
    __mss: MSSBase

    def __init__(self) -> None:
        self.__mss = mss.mss()

    def get_image_location(self, image_path: ImagePath, screenshot_path: ImagePath = None) -> ScreenRegion:
        if not screenshot_path:
            screenshot_path = self.__get_full_screen_shot_path()
        screenshot = self.__read_image_from_path(screenshot_path)
        image = self.__read_image_from_path(image_path)
        return self.__get_match_screen_region(screenshot, image)

    def __get_full_screen_shot_path(self) -> ImagePath:
        self.__mss.shot(output=self.__get_raw_image_path(self.__SCREEN_SHOT_NAME))
        return ImagePath(self.__SCREEN_SHOT_NAME)

    @staticmethod
    def __get_raw_image_path(image_name: str) -> str:
        return f'{ImagePath.get_static_dir_path()}/{image_name}'

    @staticmethod
    def __read_image_from_path(image_path: ImagePath) -> numpy.ndarray:
        return cv2.imread(image_path.value, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def __get_match_screen_region(screenshot: numpy.ndarray, template: numpy.ndarray) -> ScreenRegion:
        min_value_threshold = 0.001
        match = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)
        min_value, max_value, min_location, max_location = cv2.minMaxLoc(match)
        if min_value > min_value_threshold:
            raise ImageNotInScreenException()

        top_left_x, top_left_y = min_location
        width, height = template.shape[::-1]

        return ScreenRegion(
            top_left=Coordinates(
                x=top_left_x,
                y=top_left_y
            ),
            bottom_right=Coordinates(
                x=top_left_x + width,
                y=top_left_y + height
            )
        )

    def image_is_in_region(self, image_path: ImagePath, screen_region: ScreenRegion) -> bool:
        pass
