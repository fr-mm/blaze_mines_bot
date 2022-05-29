from unittest import TestCase

from domain.exceptions import ImageNotInScreenException
from domain.sets import ImagePathSet
from infrastructure.adapters.opencv_mss_screen_reader.opencv_template_matcher import OpencvTemplateMatcher
from tests.fixtures import ImagePathTestSet


class TestOpencvTemplateMatcher(TestCase):
    def test_locate_template_in_screenshot_WHEN_comecar_jogo_found_THEN_return_screen_region_within_expected_range(self) -> None:
        template = ImagePathSet.COMECAR_JOGO
        screenshot = ImagePathTestSet.FULL_SCREENSHOT
        opencv_template_matcher = OpencvTemplateMatcher()

        screen_region = opencv_template_matcher.locate_template_in_screenshot(
            template=template,
            screenshot=screenshot
        )

        bigger_top_left_x = 145
        bigger_top_left_y = 365
        bigger_bottom_right_x = 450
        bigger_bottom_right_y = 440
        self.assertGreater(screen_region.top_left.x, bigger_top_left_x)
        self.assertGreater(screen_region.top_left.y, bigger_top_left_y)
        self.assertLess(screen_region.bottom_right.x, bigger_bottom_right_x)
        self.assertLess(screen_region.bottom_right.y, bigger_bottom_right_y)

    def test_locate_template_in_screenshot_WHEN_comecar_jogo_found_THEN_return_screen_region_bigger_than_template(self) -> None:
        template = ImagePathSet.COMECAR_JOGO
        screenshot = ImagePathTestSet.FULL_SCREENSHOT
        opencv_template_matcher = OpencvTemplateMatcher()

        screen_region = opencv_template_matcher.locate_template_in_screenshot(
            template=template,
            screenshot=screenshot
        )

        smaller_top_left_x = 166
        smaller_top_left_y = 378
        smaller_bottom_right_x = 437
        smaller_bottom_right_y = 423
        self.assertLess(screen_region.top_left.x, smaller_top_left_x)
        self.assertLess(screen_region.top_left.y, smaller_top_left_y)
        self.assertGreater(screen_region.bottom_right.x, smaller_bottom_right_x)
        self.assertGreater(screen_region.bottom_right.y, smaller_bottom_right_y)

    def test_locate_template_in_screenshot_WHEN_money_sign_found_THEN_return_screen_region_within_expected_range(self) -> None:
        template = ImagePathSet.MONEY_SIGN
        screenshot = ImagePathTestSet.FULL_SCREENSHOT
        opencv_template_matcher = OpencvTemplateMatcher()

        screen_region = opencv_template_matcher.locate_template_in_screenshot(
            template=template,
            screenshot=screenshot
        )

        bigger_top_left_x = 197
        bigger_top_left_y = 225
        bigger_bottom_right_x = 347
        bigger_bottom_right_y = 300
        self.assertGreater(screen_region.top_left.x, bigger_top_left_x)
        self.assertGreater(screen_region.top_left.y, bigger_top_left_y)
        self.assertLess(screen_region.bottom_right.x, bigger_bottom_right_x)
        self.assertLess(screen_region.bottom_right.y, bigger_bottom_right_y)

    def test_locate_template_in_screenshot_WHEN_money_sign_found_THEN_return_screen_region_bigger_than_template(self) -> None:
        template = ImagePathSet.MONEY_SIGN
        screenshot = ImagePathTestSet.FULL_SCREENSHOT
        opencv_template_matcher = OpencvTemplateMatcher()

        screen_region = opencv_template_matcher.locate_template_in_screenshot(
            template=template,
            screenshot=screenshot
        )

        smaller_top_left_x = 226
        smaller_top_left_y = 253
        smaller_bottom_right_x = 313
        smaller_bottom_right_y = 275
        self.assertLess(screen_region.top_left.x, smaller_top_left_x)
        self.assertLess(screen_region.top_left.y, smaller_top_left_y)
        self.assertGreater(screen_region.bottom_right.x, smaller_bottom_right_x)
        self.assertGreater(screen_region.bottom_right.y, smaller_bottom_right_y)

    def test_locate_template_in_screenshot_WHEN_square_found_THEN_return_screen_region_within_expected_range(self) -> None:
        template = ImagePathSet.SQUARE
        screenshot = ImagePathTestSet.FULL_SCREENSHOT
        opencv_template_matcher = OpencvTemplateMatcher()

        screen_region = opencv_template_matcher.locate_template_in_screenshot(
            template=template,
            screenshot=screenshot
        )

        bigger_top_left_x = 705
        bigger_top_left_y = 218
        bigger_bottom_right_x = 835
        bigger_bottom_right_y = 347
        self.assertGreater(screen_region.top_left.x, bigger_top_left_x)
        self.assertGreater(screen_region.top_left.y, bigger_top_left_y)
        self.assertLess(screen_region.bottom_right.x, bigger_bottom_right_x)
        self.assertLess(screen_region.bottom_right.y, bigger_bottom_right_y)

    def test_locate_template_in_screenshot_WHEN_square_found_THEN_return_screen_region_bigger_than_template(self) -> None:
        template = ImagePathSet.SQUARE
        screenshot = ImagePathTestSet.FULL_SCREENSHOT
        opencv_template_matcher = OpencvTemplateMatcher()

        screen_region = opencv_template_matcher.locate_template_in_screenshot(
            template=template,
            screenshot=screenshot
        )
        smaller_top_left_x = 725
        smaller_top_left_y = 240
        smaller_bottom_right_x = 812
        smaller_bottom_right_y = 328
        self.assertLess(screen_region.top_left.x, smaller_top_left_x)
        self.assertLess(screen_region.top_left.y, smaller_top_left_y)
        self.assertGreater(screen_region.bottom_right.x, smaller_bottom_right_x)
        self.assertGreater(screen_region.bottom_right.y, smaller_bottom_right_y)

    def test_locate_template_in_screenshot_WHEN_comecar_jogo_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        template = ImagePathSet.COMECAR_JOGO
        screenshot = ImagePathTestSet.COMECAR_JOGO_NOT_FOUD
        opencv_template_matcher = OpencvTemplateMatcher()

        with self.assertRaises(ImageNotInScreenException):
            opencv_template_matcher.locate_template_in_screenshot(
                template=template,
                screenshot=screenshot
            )

    def test_locate_template_in_screenshot_WHEN_money_sign_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        template = ImagePathSet.MONEY_SIGN
        screenshot = ImagePathTestSet.MONEY_SIGN_NOT_FOUND
        opencv_template_matcher = OpencvTemplateMatcher()

        with self.assertRaises(ImageNotInScreenException):
            opencv_template_matcher.locate_template_in_screenshot(
                template=template,
                screenshot=screenshot
            )

    def test_locate_template_in_screenshot_WHEN_square_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        template = ImagePathSet.SQUARE
        screenshot = ImagePathTestSet.SQUARE_NOT_FOUND
        opencv_template_matcher = OpencvTemplateMatcher()

        with self.assertRaises(ImageNotInScreenException):
            opencv_template_matcher.locate_template_in_screenshot(
                template=template,
                screenshot=screenshot
            )
