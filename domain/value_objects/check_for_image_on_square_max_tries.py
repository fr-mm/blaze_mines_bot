from dataclasses import dataclass

from domain.exceptions import CheckForImageOnSquareMaxTriesException


@dataclass(frozen=True)
class CheckForImageOnSquareMaxTries:
    value: int

    def __post_init__(self) -> None:
        min_value = 1
        if self.value < min_value:
            raise CheckForImageOnSquareMaxTriesException(
                f'Must be at least {min_value}'
            )
