from abc import ABC, abstractmethod


class PrinterServicePort(ABC):
    @abstractmethod
    def print_line(self, message: str) -> None :
        pass

    @abstractmethod
    def print_open_line(self, message: str) -> None:
        pass

    @abstractmethod
    def close_line(self) -> None:
        pass
