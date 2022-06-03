from abc import ABC, abstractmethod

from domain.entities import Image


class LocateImageInScreenUseCasePort(ABC):
    @abstractmethod
    def execute(self, image: Image) -> None:
        pass
