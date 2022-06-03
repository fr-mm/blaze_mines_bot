from abc import ABC, abstractmethod

from domain.entities import Image
from domain.value_objects import ScreenRegion


class ImageIsInRegionUseCasePort(ABC):
    """If no screen region is given, uses image location"""
    @abstractmethod
    def execute(self, image: Image, screen_region: ScreenRegion = None) -> bool:
        pass

