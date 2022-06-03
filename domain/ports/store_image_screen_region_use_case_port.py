from abc import ABC, abstractmethod
from typing import Callable

from domain.value_objects import ImagePath


class StoreImageScreenRegionUseCasePort(ABC):
    @abstractmethod
    def execute(self, image: ImagePath, store_region: Callable) -> None:
        pass
