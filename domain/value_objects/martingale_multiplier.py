from dataclasses import dataclass

from domain.exceptions import MartingaleMultiplierException


@dataclass
class MartingaleMultiplier:
    __MIN_VALUE = 1
    value: float

    def __post_init__(self) -> None:
        self.__validate_positive()

    def __validate_positive(self) -> None:
        if self.value < self.__MIN_VALUE:
            raise MartingaleMultiplierException(
                f'Must be at least {self.__MIN_VALUE}'
            )
