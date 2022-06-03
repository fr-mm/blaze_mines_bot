from domain.containers import ImageIsInRegionUseCaseContainer
from domain.entities import Image
from domain.ports import ImageIsInRegionUseCasePort
from domain.value_objects import ScreenRegion


class ImageIsInRegionUseCase(ImageIsInRegionUseCasePort):
    __container: ImageIsInRegionUseCaseContainer

    def __init__(self, container: ImageIsInRegionUseCaseContainer) -> None:
        self.__container = container

    def execute(self, image: Image, screen_region: ScreenRegion = None) -> bool:
        if not screen_region:
            screen_region = self.__get_get_image_location(image=image)
        return self.__container.screen_reader.image_is_in_region(
            image=image,
            screen_region=screen_region
        )

    def __get_get_image_location(self, image: Image) -> ScreenRegion:
        if not image.location:
            self.__container.locate_image_in_screen_service.execute(image=image)
        return image.location
