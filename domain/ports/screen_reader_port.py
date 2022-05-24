from abc import ABC, abstractmethod

from domain.value_objects import ImagePath, ScreenRegion


class ScreenReaderPort(ABC):
    @abstractmethod
    def image_is_in_region(self, image_path: ImagePath, screen_region: ScreenRegion) -> bool:
        pass

    @abstractmethod
    def get_region_of_image(self, image_path: ImagePath) -> ScreenRegion or None:
        pass
