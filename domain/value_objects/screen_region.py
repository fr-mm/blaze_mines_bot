from __future__ import annotations

import ctypes

from domain.exceptions import ScreenRegionException
from domain.value_objects import Coordinates


class ScreenRegion:
    __FULL_SCREEN: ScreenRegion = None
    __top_left: Coordinates
    __bottom_right: Coordinates

    def __init__(self, top_left: Coordinates, bottom_right: Coordinates) -> None:
        self.__validate_area(top_left, bottom_right)
        self.__top_left = top_left
        self.__bottom_right = bottom_right

    @staticmethod
    def __validate_area(top_left: Coordinates, bottom_right: Coordinates) -> None:
        if top_left.x > bottom_right.x or top_left.y > bottom_right.y:
            raise ScreenRegionException(
                f'Negative area: '
                f'top_left = ({top_left.x}, {top_left.y}), '
                f'bottom_right = ({bottom_right.x}, {bottom_right.y})'
            )

    @property
    def top_left(self) -> Coordinates:
        return self.__top_left

    @property
    def bottom_right(self) -> Coordinates:
        return self.__bottom_right

    def to_string(self) -> str:
        return f'(({self.__top_left.x}, {self.__top_left.y}), ({self.__bottom_right.x}, {self.__bottom_right.y}))'

    @staticmethod
    def full_screen() -> ScreenRegion:
        if not ScreenRegion.__FULL_SCREEN:
            ScreenRegion.__FULL_SCREEN = ScreenRegion.__get_full_screen_region()
        return ScreenRegion.__FULL_SCREEN

    @staticmethod
    def __get_full_screen_region() -> ScreenRegion:
        monitor = ctypes.windll.user32
        width = monitor.GetSystemMetrics(0)
        height = monitor.GetSystemMetrics(1)
        return ScreenRegion(
            top_left=Coordinates(0, 0),
            bottom_right=Coordinates(width, height)
        )
