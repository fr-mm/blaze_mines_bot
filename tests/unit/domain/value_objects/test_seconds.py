from unittest import TestCase

from domain.exceptions import SecondsException
from domain.value_objects import Seconds


class TestSeconds(TestCase):
    def test_init_WHEN_valid_value_THEN_creates_instance(self) -> None:
        value = 1

        Seconds(value)

    def test_post_init_WHEN_negative_value_THEN_raises_invalid_seconds_exception(self) -> None:
        value = -1

        with self.assertRaises(SecondsException):
            Seconds(value)
