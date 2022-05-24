from dataclasses import dataclass

from domain.exceptions import CoordinatesException


@dataclass(frozen=True)
class Coordinates:
    x: int
    y: int

    def __post_init__(self) -> None:
        self.__validate_if_positive_values()

    def __validate_if_positive_values(self) -> None:
        if self.x < 0 or self.y < 0:
            raise CoordinatesException(
                f'Negative values: X = {self.x}, Y = {self.y}'
            )
