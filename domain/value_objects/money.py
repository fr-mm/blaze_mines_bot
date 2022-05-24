from __future__ import  annotations
from dataclasses import dataclass

from domain.exceptions import MoneyException


@dataclass(frozen=True)
class Money:
    """Stores money value in cents"""

    __CENT_SEPARATOR = ','
    __MIN_VALUE = 1
    value: int

    def __post_init__(self) -> None:
        self.__validate_greater_than_min_value()

    def __validate_greater_than_min_value(self) -> None:
        if self.value < Money.__MIN_VALUE:
            raise MoneyException(
                f'Must be at least than {self.value}'
            )

    def sum(self, money: Money) -> Money:
        new_value = self.value + money.value
        return Money(new_value)

    def to_string(self) -> str:
        min_digits = 3
        separator_index = -2

        stabilized = str(self.value).zfill(min_digits)
        return Money.__CENT_SEPARATOR.join([stabilized[:separator_index], stabilized[separator_index:]])

    @staticmethod
    def from_string(input_string: str) -> Money:
        input_string = input_string.strip()
        Money.__validate_input_string(input_string)
        value = int(''.join(input_string.split(Money.__CENT_SEPARATOR)))
        return Money(value)

    @staticmethod
    def __validate_input_string(value: str) -> None:
        min_length = 4
        separator_index = -3
        separator_count = 1

        for char in value:
            if not char.isdigit() and char != Money.__CENT_SEPARATOR:
                raise MoneyException(
                    f'Input string must only contain digits and a {Money.__CENT_SEPARATOR} separator, got {value}'
                )

        if len(value) < min_length:
            raise MoneyException(
                f'Input string must be at least {min_length} chars long, got {value}'
            )

        if value.count(Money.__CENT_SEPARATOR) != separator_count:
            raise MoneyException(
                f'Input string must have exactly {separator_count} {Money.__CENT_SEPARATOR} separator,got {value}'
            )

        if value[separator_index] != Money.__CENT_SEPARATOR:
            raise MoneyException(
                f'Input string must have a {Money.__CENT_SEPARATOR} at index {separator_index}, got {value}'
            )
