from domain.containers import GetImageScreenRegionUseCaseContainer
from domain.exceptions import ImageNotInScreenException
from domain.value_objects import ImagePath, ScreenRegion


class GetImageScreenRegionUseCase:
    __container: GetImageScreenRegionUseCaseContainer

    def __init__(self, container: GetImageScreenRegionUseCaseContainer) -> None:
        self.__container = container

    def execute(self, image_path: ImagePath) -> ScreenRegion:
        for _ in range(self.__container.max_tries.value):
            try:
                return self.__container.screen_reader.get_image_location(image_path)
            except ImageNotInScreenException:
                continue
        raise ImageNotInScreenException(
            f'Could not locate {image_path.file_name} in {self.__container.max_tries.value} tries'
        )
