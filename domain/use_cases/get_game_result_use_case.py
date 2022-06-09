import time

from domain.containers import GetGameResultUseCaseContainer
from domain.entities import Image
from domain.enums import GameResultEnum
from domain.exceptions import CheckForImageOnSquareMaxTriesException
from domain.ports import GetGameResultUseCasePort
from domain.sets.image_set import ImageSet
from domain.value_objects import ScreenRegion, Seconds, Coordinates


class GetGameResultUseCase(GetGameResultUseCasePort):
    __container: GetGameResultUseCaseContainer
    __max_tries: int
    __seconds_between_tries: Seconds

    def __init__(
            self,
            container: GetGameResultUseCaseContainer,
            max_tries: int = 200,
            seconds_between_tries: Seconds = Seconds(0.5)
    ) -> None:
        self.__container = container
        self.__max_tries = max_tries
        self.__seconds_between_tries = seconds_between_tries

    def execute(self) -> GameResultEnum:
        for _ in range(self.__max_tries):
            if self.__image_is_in_square_region(ImageSet.DIAMOND):
                return GameResultEnum.WIN
            elif self.__image_is_in_square_region(ImageSet.BOMB):
                return GameResultEnum.LOSS
            else:
                self.__locate_diamond_or_bomb()
                time.sleep(self.__seconds_between_tries.value)
        raise CheckForImageOnSquareMaxTriesException(
            f'{ImageSet.DIAMOND.name.value} ou {ImageSet.BOMB.name.value} não encontrados em {self.__max_tries} tentativas'
        )

    def __image_is_in_square_region(self, image: Image) -> bool:
        return self.__container.image_is_in_region_service.execute(
                image=image,
                screen_region=ImageSet.SQUARE.location
        )

    def __locate_diamond_or_bomb(self) -> bool:
        if not self.__set_square_location_to_other_image_location(ImageSet.DIAMOND):
            if not self.__set_square_location_to_other_image_location(ImageSet.BOMB):
                return False
        return True

    def __set_square_location_to_other_image_location(self, image: Image) -> bool:
        if self.__container.image_is_in_region_service.execute(
                image=image,
                screen_region=ScreenRegion.full_screen()
        ):
            self.__container.locate_image_in_screen_service.execute(image=image)
            ImageSet.SQUARE.location = self.__resize_screen_region_to_square_size(image.location)
            return True
        return False

    @staticmethod
    def __resize_screen_region_to_square_size(original_screen_region: ScreenRegion) -> ScreenRegion:
        half_width = round(ImageSet.SQUARE.location.width / 2)
        half_height = round(ImageSet.SQUARE.location.height / 2)
        return ScreenRegion(
            top_left=Coordinates(
                x=original_screen_region.center.x - half_width,
                y=original_screen_region.center.y - half_height
            ),
            bottom_right=Coordinates(
                x=original_screen_region.center.x + half_width,
                y=original_screen_region.center.y + half_height
            )
        )
