from domain.ports import PrinterServicePort


class PrinterService(PrinterServicePort):
    def print(self, message: str) -> None:
        print(message)
