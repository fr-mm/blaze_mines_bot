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
