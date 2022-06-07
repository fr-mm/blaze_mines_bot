from abc import ABC, abstractmethod

from domain.enums import GameResultEnum


class GetGameResultUseCasePort(ABC):
    @abstractmethod
    def execute(self) -> GameResultEnum:
        pass
