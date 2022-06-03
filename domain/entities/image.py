from domain.exceptions import ImageLocationNotSetException
from domain.value_objects import ImagePath, ScreenRegion, ImageName


class Image:
    __name: ImageName
    __path: ImagePath
    __location: ScreenRegion or None

    def __init__(
            self,
            name: ImageName,
            path: ImagePath,
            location: ScreenRegion = None
    ) -> None:
        self.__name = name
        self.__path = path
        self.__location = location

    @property
    def name(self) -> ImageName:
        return self.__name

    @property
    def path(self) -> ImagePath:
        return self.__path

    @property
    def location(self) -> ScreenRegion or None:
        self.__validate_location_is_set()
        return self.__location

    @location.setter
    def location(self, screen_region: ScreenRegion) -> None:
        self.__location = screen_region

    def __validate_location_is_set(self) -> None:
        if not self.__location:
            raise ImageLocationNotSetException(
                f'{self.__name} location not set'
            )
