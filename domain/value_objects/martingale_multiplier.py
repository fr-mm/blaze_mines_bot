from __future__ import annotations
from dataclasses import dataclass

from domain.enums import NumberFormatEnum
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

    def to_string(self) -> str:
        separator = NumberFormatEnum.DECIMAL_SEPARATOR.value
        return str(self.value).replace('.', separator).replace(',', separator)

    @staticmethod
    def from_string(value: str) -> MartingaleMultiplier:
        value = value.replace(',', '.')
        try:
            return MartingaleMultiplier(float(value))
        except ValueError:
            raise MartingaleMultiplierException(
                f'Can not convert {value} to float'
            )
