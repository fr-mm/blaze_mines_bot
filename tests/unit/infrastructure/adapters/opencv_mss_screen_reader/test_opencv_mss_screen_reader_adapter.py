from unittest import TestCase

from mockito import when, unstub

from domain.exceptions import ImageNotInScreenException
from domain.sets import ImagePathSet
from domain.value_objects import ScreenRegion, Coordinates
from domain.value_objects import image_path
from infrastructure.adapters import OpencvMssScreenReaderAdapter
from tests.fixtures import ImagePathTestSet


class TestOpencvMssScreenReaderAdapter(TestCase):
    def tearDown(self) -> None:
        unstub()

    def test_get_image_location_WHEN_comecar_jogo_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        template_path = ImagePathSet.COMECAR_JOGO
        screenshot_path = ImagePathTestSet.COMECAR_JOGO_NOT_FOUD
        screen_reader = OpencvMssScreenReaderAdapter()
        
        with self.assertRaises(ImageNotInScreenException):
            screen_reader.get_image_location(
                image_path=template_path,
                screenshot_path=screenshot_path
            )

    def test_get_image_location_WHEN_comecar_jogo_found_THEN_does_not_raise_exception(self) -> None:
        template_path = ImagePathSet.COMECAR_JOGO
        screenshot_path = ImagePathTestSet.INITIAL_SCREEN
        screen_reader = OpencvMssScreenReaderAdapter()

        screen_reader.get_image_location(
            image_path=template_path,
            screenshot_path=screenshot_path
        )

    def test_get_image_location_WHEN_comecar_jogo_found_THEN_returns_screen_region_containing_image_center_point(self) -> None:
        template_path = ImagePathSet.COMECAR_JOGO
        screenshot_path = ImagePathTestSet.INITIAL_SCREEN
        center_x, center_y = 300, 440
        screen_reader = OpencvMssScreenReaderAdapter()

        screen_region = screen_reader.get_image_location(
            image_path=template_path,
            screenshot_path=screenshot_path
        )

        self.assertLess(screen_region.top_left.x, center_x)
        self.assertLess(screen_region.top_left.y, center_y)
        self.assertGreater(screen_region.bottom_right.x, center_x)
        self.assertGreater(screen_region.bottom_right.y, center_y)

    def test_get_image_location_WHEN_money_sign_found_THEN_returns_region_containing_image_center(self) -> None:
        template_path = ImagePathSet.MONEY_SIGN
        screenshot_path = ImagePathTestSet.INITIAL_SCREEN
        center_x, center_y = 260, 300
        screen_reader = OpencvMssScreenReaderAdapter()

        screen_region = screen_reader.get_image_location(
            image_path=template_path,
            screenshot_path=screenshot_path
        )

        self.assertLess(screen_region.top_left.x, center_x)
        self.assertLess(screen_region.top_left.y, center_y)
        self.assertGreater(screen_region.bottom_right.x, center_x)
        self.assertGreater(screen_region.bottom_right.y, center_y)

    def test_get_image_location_WHEN_money_sign_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        template_path = ImagePathSet.MONEY_SIGN
        screenshot_path = ImagePathTestSet.MONEY_SIGN_NOT_FOUND
        screen_reader = OpencvMssScreenReaderAdapter()

        with self.assertRaises(ImageNotInScreenException):
            screen_reader.get_image_location(
                image_path=template_path,
                screenshot_path=screenshot_path
            )

    def test_get_image_location_WHEN_right_square_found_THEN_returns_region_containing_image_center(self) -> None:
        template_path = ImagePathSet.SQUARE
        screenshot_path = ImagePathTestSet.INITIAL_SCREEN
        center_x, center_y = 773, 324
        screen_reader = OpencvMssScreenReaderAdapter()

        screen_region = screen_reader.get_image_location(
            image_path=template_path,
            screenshot_path=screenshot_path
        )

        self.assertLess(screen_region.top_left.x, center_x)
        self.assertLess(screen_region.top_left.y, center_y)
        self.assertGreater(screen_region.bottom_right.x, center_x)
        self.assertGreater(screen_region.bottom_right.y, center_y)

    def test_image_is_in_region_WHEN_image_found_THEN_return_true(self) -> None:
        screenshot_name = 'screenshot.png'
        template_path = ImagePathSet.DIAMOND
        screen_region = ScreenRegion(
            Coordinates(1, 2),
            Coordinates(3, 4)
        )
        when(image_path).ImagePath(screenshot_name).thenReturn(ImagePathSet.DIAMOND)
        screen_reader = OpencvMssScreenReaderAdapter()

        result = screen_reader.image_is_in_region(
            image_path=template_path,
            screen_region=screen_region
        )

        self.assertTrue(result)

    def test_image_is_in_region_WHEN_image_not_found_THEN_return_false(self) -> None:
        screenshot_name = 'screenshot.png'
        template_path = ImagePathSet.DIAMOND
        screen_region = ScreenRegion(
            Coordinates(1, 2),
            Coordinates(3, 4)
        )
        when(image_path).ImagePath(screenshot_name).thenReturn(ImagePathSet.BOMB)
        screen_reader = OpencvMssScreenReaderAdapter()

        result = screen_reader.image_is_in_region(
            image_path=template_path,
            screen_region=screen_region
        )

        self.assertFalse(result)