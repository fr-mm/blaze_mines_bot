from abc import ABC, abstractmethod

from domain.aggregates import Config


class ConfigSetterInterfacePort(ABC):
    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def user_inputs_are_valid(self) -> bool:
        pass

    @abstractmethod
    def get_config(self) -> Config:
        pass
