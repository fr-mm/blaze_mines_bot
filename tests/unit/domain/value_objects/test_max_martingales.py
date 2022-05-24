from unittest import TestCase

from domain.exceptions import MaxMartingalesException
from domain.value_objects import MaxMartingales


class TestMaxMartingales(TestCase):
    def test_init_WHEN_valid_value_THEN_creates_instance(self) -> None:
        value = 0

        MaxMartingales(value)

    def test_post_init_WHEN_value_less_than_min_THEN_raises_max_martingales_exception(self) -> None:
        value = -1

        with self.assertRaises(MaxMartingalesException):
            MaxMartingales(value)

    def test_to_string_WHEN_called_THEN_returns_expected_string(self) -> None:
        max_martingales = MaxMartingales(3)

        result_string = max_martingales.to_string()

        expected_string = '3'
        self.assertEqual(result_string, expected_string)

    def test_from_string_WHEN_string_is_valid_THEN_returns_expected_max_martingales(self) -> None:
        input_string = '3'

        result_max_martingales = MaxMartingales.from_string(input_string)

        expected_max_martingales = MaxMartingales(3)
        self.assertEqual(result_max_martingales, expected_max_martingales)

    def test_from_string_WHEN_string_is_invalid_THEN_raises_max_martingales_exception(self) -> None:
        input_string = 'foo'

        with self.assertRaises(MaxMartingalesException):
            MaxMartingales.from_string(input_string)
