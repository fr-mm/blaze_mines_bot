from abc import ABC, abstractmethod

from domain.value_objects import Coordinates, ScreenRegion


class ClickerPort(ABC):
    @abstractmethod
    def click_on_coordinates(self, coordinates: Coordinates) -> None:
        pass

    @abstractmethod
    def click_on_screen_region(self, screen_region: ScreenRegion) -> None:
        pass
