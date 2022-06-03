import time
from typing import Callable

from domain.containers.store_image_screen_region_use_case_container import StoreImageScreenRegionUseCaseContainer
from domain.exceptions import ImageNotInScreenException
from domain.ports import StoreImageScreenRegionUseCasePort
from domain.value_objects import ImagePath


class StoreImageScreenRegionUseCase(StoreImageScreenRegionUseCasePort):
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

    def execute(self, image: ImagePath, store_region: Callable) -> None:
        for try_count in range(1, self.__max_tries + 1):
            try:
                screen_region = self.__container.screen_reader.get_image_location(image)
                self.__container.printer.close_line()
                self.__container.printer.print_line(
                    f'{image.file_name} localizado: {screen_region.to_string()}'
                )
                store_region(screen_region)
                return

            except ImageNotInScreenException:
                self.__container.printer.print_open_line(
                    f'{image.file_name} não localizado ({try_count})'
                )
                time.sleep(self.__seconds_between_tries)
                continue

        error_message = f'{image.file_name} não localizado em {self.__max_tries} tentativas'
        self.__container.printer.close_line()
        self.__container.printer.print_line(error_message)
        raise ImageNotInScreenException(error_message)
