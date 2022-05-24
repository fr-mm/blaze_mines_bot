from __future__ import annotations
from dataclasses import dataclass

from domain.enums import NumberFormatEnum
from domain.exceptions import SecondsException


@dataclass(frozen=True)
class Seconds:
    value: float

    def __post_init__(self) -> None:
        self.__validate_not_negative()

    def __validate_not_negative(self) -> None:
        if self.value < 0:
            raise SecondsException(
                f'Seconds must not be negative, got {self.value}'
            )

    def to_string(self) -> str:
        separator = NumberFormatEnum.DECIMAL_SEPARATOR.value
        return str(self.value).replace('.', separator).replace(',', separator)

    @staticmethod
    def from_string(value) -> Seconds:
        value = value.replace(',', '.')
        try:
            return Seconds(float(value))
        except ValueError:
            raise SecondsException(
                f'Can not convert {value} to float'
            )
