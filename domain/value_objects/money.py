from __future__ import  annotations
from dataclasses import dataclass

from domain.enums import NumberFormatEnum
from domain.exceptions import MoneyException
from domain.value_objects.martingale_multiplier import MartingaleMultiplier


@dataclass(frozen=True)
class Money:
    """Stores money value in cents"""

    value: int

    def __post_init__(self) -> None:
        self.__validate_greater_than_min_value()

    def __validate_greater_than_min_value(self) -> None:
        min_value = 1
        if self.value < min_value:
            raise MoneyException(
                f'Must be at least than {self.value}'
            )

    def sum(self, money: Money) -> Money:
        new_value = self.value + money.value
        return Money(new_value)

    def multiply(self, martingale_multiplier: MartingaleMultiplier) -> Money:
        new_value = round(self.value * martingale_multiplier.value)
        return Money(new_value)

    def to_string(self) -> str:
        min_digits = 3
        separator_index = -2
        separator = NumberFormatEnum.DECIMAL_SEPARATOR.value

        stabilized = str(self.value).zfill(min_digits)
        return separator.join([stabilized[:separator_index], stabilized[separator_index:]])

    @staticmethod
    def from_string(input_string: str) -> Money:
        separator = NumberFormatEnum.DECIMAL_SEPARATOR.value
        input_string = input_string.strip()
        Money.__validate_input_string(input_string)
        value = int(''.join(input_string.split(separator)))
        return Money(value)

    @staticmethod
    def __validate_input_string(value: str) -> None:
        min_length = 4
        separator_index = -3
        separator_count = 1
        separator = NumberFormatEnum.DECIMAL_SEPARATOR.value

        for char in value:
            if not char.isdigit() and char != separator:
                raise MoneyException(
                    f'Input string must only contain digits and a {separator} separator, got {value}'
                )

        if len(value) < min_length:
            raise MoneyException(
                f'Input string must be at least {min_length} chars long, got {value}'
            )

        if value.count(separator) != separator_count:
            raise MoneyException(
                f'Input string must have exactly {separator_count} {separator} separator,got {value}'
            )

        if value[separator_index] != separator:
            raise MoneyException(
                f'Input string must have a {separator} at index {separator_index}, got {value}'
            )
