from abc import ABC, abstractmethod


class RunProgramUseCasePort(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
