from unittest import TestCase

from mockito import mock, unstub, when, verify

from domain.containers import GetGameResultUseCaseContainer
from domain.enums import GameResultEnum
from domain.ports import ImageIsInRegionUseCasePort, LocateImageInScreenUseCasePort
from domain.sets.image_set import ImageSet
from domain.use_cases import GetGameResultUseCase
from domain.value_objects import Seconds, ScreenRegion


class TestGetGameResultsUseCase(TestCase):
    def setUp(self) -> None:
        self.image_is_in_region_service = mock(ImageIsInRegionUseCasePort)
        self.locate_image_in_screen_service = mock(LocateImageInScreenUseCasePort)
        self.container = GetGameResultUseCaseContainer(
            image_is_in_region_service=self.image_is_in_region_service,
            locate_image_in_screen_service=self.locate_image_in_screen_service
        )
        self.max_tries = 1
        self.seconds_between_tries = Seconds(0)
        self.square_location = mock(ScreenRegion)
        ImageSet.SQUARE.location = self.square_location

    def tearDown(self) -> None:
        ImageSet.SQUARE.location = None
        ImageSet.DIAMOND.location = None
        ImageSet.BOMB.location = None
        unstub()

    def test_execute_WHEN_diamond_found_in_square_region_THEN_return_win(self) -> None:
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=self.square_location
        ).thenReturn(True)
        get_game_result_use_case = GetGameResultUseCase(
            container=self.container,
            max_tries=self.max_tries,
            seconds_between_tries=self.seconds_between_tries
        )

        game_result = get_game_result_use_case.execute()

        expected_game_result = GameResultEnum.WIN
        self.assertEqual(game_result, expected_game_result)

    def test_execute_WHEN_bomb_in_square_region_found_THEN_return_loss(self) -> None:
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=self.square_location
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.BOMB,
            screen_region=self.square_location
        ).thenReturn(True)
        get_game_result_use_case = GetGameResultUseCase(
            container=self.container,
            max_tries=self.max_tries,
            seconds_between_tries=self.seconds_between_tries
        )

        game_result = get_game_result_use_case.execute()

        expected_game_result = GameResultEnum.LOSS
        self.assertEqual(game_result, expected_game_result)

    def test_execute_WHEN_bomb_and_diamond_not_found_in_square_region_but_diamond_is_in_screen_THEN_sets_diamond_location_to_square_location(self) -> None:
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=self.square_location
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.BOMB,
            screen_region=self.square_location
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=ScreenRegion.full_screen()
        ).thenReturn(True)
        when(self.locate_image_in_screen_service).execute(image=ImageSet.DIAMOND)
        diamond_location = mock(ScreenRegion)
        ImageSet.DIAMOND.location = diamond_location
        get_game_result_use_case = GetGameResultUseCase(
            container=self.container,
            max_tries=self.max_tries,
            seconds_between_tries=self.seconds_between_tries
        )

        get_game_result_use_case.execute()

        expected_square_location = diamond_location
        self.assertEqual(ImageSet.SQUARE.location, expected_square_location)

    def test_execute_WHEN_bomb_and_diamond_not_found_in_square_region_but_bomb_is_in_screen_THEN_sets_bomb_location_to_square_location(self) -> None:
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=self.square_location
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.BOMB,
            screen_region=self.square_location
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=ScreenRegion.full_screen()
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.BOMB,
            screen_region=ScreenRegion.full_screen()
        ).thenReturn(True)
        when(self.locate_image_in_screen_service).execute(image=ImageSet.DIAMOND)
        when(self.locate_image_in_screen_service).execute(image=ImageSet.BOMB)
        bomb_location = mock(ScreenRegion)
        ImageSet.BOMB.location = bomb_location
        get_game_result_use_case = GetGameResultUseCase(
            container=self.container,
            max_tries=self.max_tries,
            seconds_between_tries=self.seconds_between_tries
        )

        get_game_result_use_case.execute()

        expected_square_location = bomb_location
        self.assertEqual(ImageSet.SQUARE.location, expected_square_location)

    def test_execute_WHEN_bomb_and_diamond_not_in_screen_THEN_try_again(self) -> None:
        max_tries = 2
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=self.square_location
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.BOMB,
            screen_region=self.square_location
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.DIAMOND,
            screen_region=ScreenRegion.full_screen()
        ).thenReturn(False)
        when(self.image_is_in_region_service).execute(
            image=ImageSet.BOMB,
            screen_region=ScreenRegion.full_screen()
        ).thenReturn(False)
        get_game_result_use_case = GetGameResultUseCase(
            container=self.container,
            max_tries=max_tries,
            seconds_between_tries=self.seconds_between_tries
        )

        get_game_result_use_case.execute()

        verify(self.image_is_in_region_service, times=max_tries).execute(
            image=ImageSet.DIAMOND,
            screen_region=self.square_location
        )
