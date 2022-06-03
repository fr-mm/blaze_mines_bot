import os
from unittest import TestCase

from infrastructure.adapters.opencv_mss_screen_reader.mss_screenshooter import MssScreenshooter


class TestMssScreenshooter(TestCase):
    def setUp(self) -> None:
        self.remove_screenshot()

    def tearDown(self) -> None:
        self.remove_screenshot()

    @staticmethod
    def remove_screenshot() -> None:
        screenshot = MssScreenshooter.get_path()
        if os.path.isfile(screenshot):
            os.remove(screenshot)

    def test_take_full_screenshot_WHEN_called_THEN_creates_image_file(self) -> None:
        mss_screenshooter = MssScreenshooter()

        mss_screenshooter.take_full_screenshot()

        image_path = mss_screenshooter.get_path()
        self.assertTrue(os.path.isfile(image_path))

    def test_take_full_screenshot_WHEN_called_THEN_returns_expected_image_with_expected_path_value(self) -> None:
        mss_screenshooter = MssScreenshooter()

        image = mss_screenshooter.take_full_screenshot()

        expected_value = mss_screenshooter.get_path()
        self.assertEqual(image.path.value, expected_value)
