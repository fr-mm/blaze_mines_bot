from abc import ABC


class PrinterServicePort(ABC):
    def print(self, message: str) -> None :
        pass
