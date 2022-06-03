import time

from domain.containers.get_image_screen_region_use_case_container import GetImageScreenRegionUseCaseContainer
from domain.exceptions import ImageNotInScreenException
from domain.ports import GetImageScreenRegionUseCasePort
from domain.value_objects import ImagePath, ScreenRegion


class GetImageScreenRegionUseCase(GetImageScreenRegionUseCasePort):
    __container: GetImageScreenRegionUseCaseContainer

    def __init__(self, container: GetImageScreenRegionUseCaseContainer) -> None:
        self.__container = container

    def execute(self, image_path: ImagePath) -> ScreenRegion:
        for try_count in range(self.__container.max_tries.value):
            try:
                return self.__container.screen_reader.get_image_location(image_path)
            except ImageNotInScreenException:
                self.__container.printer.print(f'{image_path.file_name} não localizado ({try_count}) tentativas  ')
                time.sleep(1)
                continue
        raise ImageNotInScreenException(
            f'Could not locate {image_path.file_name} in {self.__container.max_tries.value} tries'
        )
