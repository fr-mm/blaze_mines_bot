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
