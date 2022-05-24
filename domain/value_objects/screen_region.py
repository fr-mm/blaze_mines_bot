from dataclasses import dataclass

from domain.exceptions import InvalidScreenRegionException
from domain.value_objects import Coordinates


@dataclass(frozen=True)
class ScreenRegion:
    top_left: Coordinates
    bottom_right: Coordinates

    def __post_init__(self) -> None:
        self.__validate_area_is_positive()

    def __validate_area_is_positive(self) -> None:
        if self.top_left.x > self.bottom_right.x or self.top_left.y > self.bottom_right.y:
            raise InvalidScreenRegionException(
                f'Negative area: '
                f'top_left = ({self.top_left.x}, {self.top_left.y}), '
                f'bottom_right = ({self.bottom_right.x}, {self.bottom_right.y})'
            )
