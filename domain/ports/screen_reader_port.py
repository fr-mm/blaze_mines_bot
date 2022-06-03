from abc import ABC, abstractmethod

from domain.entities import Image
from domain.value_objects import ScreenRegion


class ScreenReaderPort(ABC):
    @abstractmethod
    def get_image_location(self, image: Image) -> ScreenRegion:
        pass

    @abstractmethod
    def image_is_in_region(self, image: Image, screen_region: ScreenRegion) -> bool:
        pass
