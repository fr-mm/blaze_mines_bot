from abc import ABC, abstractmethod


class RunProgramUseCasePort(ABC):
    @abstractmethod
    def execute(self, loop_forever: bool = True) -> None:
        pass
