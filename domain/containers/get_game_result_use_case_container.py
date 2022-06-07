from dataclasses import dataclass

from domain.ports import ImageIsInRegionUseCasePort, LocateImageInScreenUseCasePort


@dataclass(frozen=True)
class GetGameResultUseCaseContainer:
    image_is_in_region_service: ImageIsInRegionUseCasePort
    locate_image_in_screen_service: LocateImageInScreenUseCasePort
