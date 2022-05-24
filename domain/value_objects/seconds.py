from dataclasses import dataclass

from domain.exceptions import InvalidSecondsException


@dataclass(frozen=True)
class Seconds:
    value: float

    def __post_init__(self) -> None:
        self.__validate_not_negative()

    def __validate_not_negative(self) -> None:
        if self.value < 0:
            raise InvalidSecondsException(
                f'Seconds must not be negative, got {self.value}'
            )
