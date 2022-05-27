from __future__ import annotations

from dataclasses import dataclass

from domain.enums import NumberFormatEnum
from domain.value_objects.money import Money


@dataclass(frozen=True)
class Profit:
    """Store profit value in cents"""

    value: int

    def sum(self, money: Money) -> Profit:
        return Profit(self.value + money.value)

    def subtract(self, money: Money) -> Profit:
        return Profit(self.value - money.value)

    def to_string(self) -> str:
        value = self.value
        minus_placeholder = ''

        if value < 0:
            value *= -1
            minus_placeholder = '-'

        string_value = str(value).rjust(3, '0')

        decimal_part = string_value[-2:]
        integer_part = string_value[:-2]
        integer_part = minus_placeholder + integer_part
        separator = NumberFormatEnum.DECIMAL_SEPARATOR.value

        return separator.join([integer_part, decimal_part])
