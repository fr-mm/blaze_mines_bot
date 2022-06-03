from dataclasses import dataclass

from domain.exceptions import ImageNameException


@dataclass(frozen=True)
class ImageName:
    value: str

    def __post_init__(self) -> None:
        self.__validate_not_empty()

    def __validate_not_empty(self) -> None:
        if not self.value:
            raise ImageNameException(
                'Can not be an empty string'
            )
