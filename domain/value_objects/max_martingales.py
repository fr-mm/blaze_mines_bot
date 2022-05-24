from dataclasses import dataclass

from domain.exceptions import MaxMartingalesException


@dataclass
class MaxMartingales:
    __MIN_VALUE = 0
    value: int

    def __post_init__(self) -> None:
        self.__validate_min_value()

    def __validate_min_value(self) -> None:
        if self.value < self.__MIN_VALUE:
            raise MaxMartingalesException(
                f'Must be at least {self.__MIN_VALUE}'
            )
