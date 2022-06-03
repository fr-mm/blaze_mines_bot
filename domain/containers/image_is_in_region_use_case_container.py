from dataclasses import dataclass

from domain.ports import LocateImageInScreenUseCasePort, ScreenReaderPort


@dataclass(frozen=True)
class ImageIsInRegionUseCaseContainer:
    locate_image_in_screen_service: LocateImageInScreenUseCasePort
    screen_reader: ScreenReaderPort
