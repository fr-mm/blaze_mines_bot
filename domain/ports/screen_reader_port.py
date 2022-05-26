from abc import ABC, abstractmethod

from domain.value_objects import ImagePath, ScreenRegion


class ScreenReaderPort(ABC):
    @abstractmethod
    def get_image_location(self, image_path: ImagePath) -> ScreenRegion:
        pass

    @abstractmethod
    def image_is_in_region(self, image_path: ImagePath, screen_region: ScreenRegion) -> bool:
        pass
