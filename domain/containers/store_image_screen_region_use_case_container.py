from dataclasses import dataclass

from domain.ports import ScreenReaderPort, PrinterServicePort


@dataclass(frozen=True)
class StoreImageScreenRegionUseCaseContainer:
    screen_reader: ScreenReaderPort
    printer: PrinterServicePort
