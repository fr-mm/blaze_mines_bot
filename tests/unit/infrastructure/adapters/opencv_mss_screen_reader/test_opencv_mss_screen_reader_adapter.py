from unittest import TestCase

from domain.exceptions import ImageNotInScreenException
from domain.sets import ImagePathSet
from infrastructure.adapters.opencv_mss_screen_reader.opencv_mss_screen_reader_adapter import \
    OpencvMssScreenReaderAdapter
from tests.fixtures import ImagePathTestSet


class TestOpencvMssScreenReaderAdapter(TestCase):
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
