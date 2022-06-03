from domain.ports import PrinterServicePort


class PrinterService(PrinterServicePort):
    __open_line: bool

    def __init__(self) -> None:
        self.__open_line = False

    def print_line(self, message: str) -> None:
        print(message)

    def print_open_line(self, message: str) -> None:
        print(f'\r{message}', end='')
        self.__open_line = True

    def close_line(self) -> None:
        if self.__open_line:
            print('\n')
            self.__open_line = False
