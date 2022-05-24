from abc import ABC, abstractmethod

from domain.value_objects import Coordinates


class ClickerPort(ABC):
    @abstractmethod
    def click_on(self, coordinates: Coordinates) -> None:
        pass
