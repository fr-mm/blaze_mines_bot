from abc import ABC, abstractmethod

from domain.value_objects import ImagePath, ScreenRegion


class GetImageScreenRegionUseCasePort(ABC):
    @abstractmethod
    def execute(self, image_path: ImagePath) -> ScreenRegion:
        pass
