from dataclasses import dataclass

from domain.exceptions import LocateImageMaxTriesException


@dataclass(frozen=True)
class LocateImageMaxTries:
    value: int

    def __post_init__(self) -> None:
        min_value = 1
        if self.value < min_value:
            raise LocateImageMaxTriesException(
                f'Must be at least {min_value}'
            )
