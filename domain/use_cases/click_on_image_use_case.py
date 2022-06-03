from domain.containers import ClickOnImageUseCaseContainer
from domain.entities import Image
from domain.ports import ClickOnImageUseCasePort


class ClickOnImageUseCase(ClickOnImageUseCasePort):
    __container: ClickOnImageUseCaseContainer

    def __init__(self, container: ClickOnImageUseCaseContainer) -> None:
        self.__container = container

    def execute(self, image: Image) -> None:
        if not image.location or not self.__container.image_is_in_region_service.execute(image):
            self.__container.locate_image_in_screen_service.execute(image)
        self.__container.clicker.click_on_screen_region(image.location)
