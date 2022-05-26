from abc import ABC, abstractmethod

from domain.value_objects import Money


class TyperPort(ABC):
    @abstractmethod
    def __init__(self, seconds_between_keystrokes: float) -> None:
        pass

    @abstractmethod
    def type_money(self, money: Money) -> None:
        pass
