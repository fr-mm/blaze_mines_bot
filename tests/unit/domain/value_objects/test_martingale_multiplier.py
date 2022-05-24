from unittest import TestCase

from domain.exceptions import MartingaleMultiplierException
from domain.value_objects import MartingaleMultiplier


class TestMartingaleMultiplier(TestCase):
    def test_init_WHEN_valid_value_THEN_creates_instance(self) -> None:
        value = 1.5

        MartingaleMultiplier(value)

    def test_post_init_WHEN_value_is_lower_than_min_THEN_raises_martingale_multiplier_exception(self) -> None:
        value = 0.5

        with self.assertRaises(MartingaleMultiplierException):
            MartingaleMultiplier(value)

    def test_to_string_WHEN_called_THEN_returns_expected_string(self) -> None:
        martingale_multiplier = MartingaleMultiplier(1.5)

        result_string = martingale_multiplier.to_string()

        expected_string = '1,5'
        self.assertEqual(result_string, expected_string)

    def test_from_string_WHEN_string_has_comma_THEN_returns_expected_martingale_multiplier(self) -> None:
        input_string = '12,34'

        result_martingale_multiplier = MartingaleMultiplier.from_string(input_string)

        expected_martingale_multiplier = MartingaleMultiplier(12.34)
        self.assertEqual(result_martingale_multiplier, expected_martingale_multiplier)

    def test_from_string_WHEN_string_is_invalid_THEN_raises_martingale_multiplier_exception(self) -> None:
        input_string = 'foo'

        with self.assertRaises(MartingaleMultiplierException):
            MartingaleMultiplier.from_string(input_string)
