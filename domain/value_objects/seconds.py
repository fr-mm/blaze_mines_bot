from dataclasses import dataclass

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
