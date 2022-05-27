from unittest import TestCase

from domain.exceptions import CheckForImageOnSquareMaxTriesException
from domain.value_objects import CheckForImageOnSquareMaxTries


class TestCheckForImageOnSquareMaxTries(TestCase):
    def test_post_init_WHEN_value_is_valid_THEN_returns_instance(self) -> None:
        value = 1

        CheckForImageOnSquareMaxTries(value)

    def test_post_init_WHEN_value_is_less_then_min_THEN_raises_locate_image_max_tries_exception(self) -> None:
        value = 0

        with self.assertRaises(CheckForImageOnSquareMaxTriesException):
            CheckForImageOnSquareMaxTries(value)
