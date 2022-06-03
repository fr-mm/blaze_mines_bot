from dataclasses import dataclass

from domain.ports import ClickerPort, LocateImageInScreenUseCasePort, ImageIsInRegionUseCasePort


@dataclass(frozen=True)
class ClickOnImageUseCaseContainer:
    clicker: ClickerPort
    locate_image_in_screen_service: LocateImageInScreenUseCasePort
    image_is_in_region_service: ImageIsInRegionUseCasePort
