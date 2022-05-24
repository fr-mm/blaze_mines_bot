from abc import ABC, abstractmethod

from domain.aggregates import Config


class ConfigSetterInterfacePort(ABC):
    @abstractmethod
    def prompt_user_config(self) -> Config:
        pass
