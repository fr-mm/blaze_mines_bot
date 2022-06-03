from abc import ABC, abstractmethod
from typing import Callable

from domain.entities import Image


class ClickOnImageUseCasePort(ABC):
    @abstractmethod
    def execute(self, image: Image) -> None:
        pass

