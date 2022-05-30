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

    def test_to_string_WHEN_called_THEN_returns_expected_string(self) -> None:
        seconds = Seconds(1.5)

        result_string = seconds.to_string()

        expected_string = '1.5'
        self.assertEqual(result_string, expected_string)

    def test_from_string_WHEN_string_has_comma_THEN_returns_expected_seconds(self) -> None:
        input_string = '12.34'

        result_seconds = Seconds.from_string(input_string)

        expected_martingale_multiplier = Seconds(12.34)
        self.assertEqual(result_seconds, expected_martingale_multiplier)

    def test_from_string_WHEN_string_is_invalid_THEN_raises_seconds_exception(self) -> None:
        input_string = 'foo'

        with self.assertRaises(SecondsException):
            Seconds.from_string(input_string)

