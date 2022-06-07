import time

from domain.containers.store_image_screen_region_use_case_container import StoreImageScreenRegionUseCaseContainer
from domain.entities import Image
from domain.exceptions import ImageNotInScreenException
from domain.ports import LocateImageInScreenUseCasePort


class LocateImageInScreenUseCase(LocateImageInScreenUseCasePort):
    __container: StoreImageScreenRegionUseCaseContainer
    __max_tries: int
    __seconds_between_tries: float

    def __init__(
            self,
            container: StoreImageScreenRegionUseCaseContainer,
            max_tries: int = 200,
            seconds_between_tries: float = 0.6
    ) -> None:
        self.__container = container
        self.__max_tries = max_tries
        self.__seconds_between_tries = seconds_between_tries

    def execute(self, image: Image) -> None:
        for try_count in range(self.__max_tries):
            try:
                image.location = self.__container.screen_reader.get_image_location(image)
                self.__container.printer.close_line()
                self.__container.printer.print_line(
                    f'{image.name.value} localizado: {image.location.to_string()}'
                )
                return

            except ImageNotInScreenException:
                image.location = None
                self.__container.printer.print_open_line(
                    f'{image.name.value} não localizado ({try_count + 1})'
                )
                time.sleep(self.__seconds_between_tries)
                continue

        error_message = f'{image.name.value} não localizado em {self.__max_tries} tentativas'
        self.__container.printer.close_line()
        self.__container.printer.print_line(error_message)
        raise ImageNotInScreenException(error_message)
