from dataclasses import dataclass

from domain.ports import ClickerPort, StoreImageScreenRegionUseCasePort


@dataclass(frozen=True)
class ClickOnImageUseCaseContainer:
    clicker: ClickerPort
    store_image_screen_region_service: StoreImageScreenRegionUseCasePort
