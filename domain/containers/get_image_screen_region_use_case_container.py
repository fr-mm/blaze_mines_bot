from dataclasses import dataclass

from domain.ports import ScreenReaderPort, PrinterServicePort
from domain.value_objects import LocateImageMaxTries, Seconds


@dataclass(frozen=True)
class GetImageScreenRegionUseCaseContainer:
    screen_reader: ScreenReaderPort
    max_tries: LocateImageMaxTries
    printer: PrinterServicePort
    seconds_between_tries: Seconds = Seconds(0.2)
