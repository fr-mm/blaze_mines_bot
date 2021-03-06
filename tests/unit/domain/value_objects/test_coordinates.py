from unittest import TestCase

from domain.exceptions import CoordinatesException
from domain.value_objects import Coordinates


class TestCoordinates(TestCase):
    def test_init_WHEN_coordinates_are_positive_THEN_creates_instance(self) -> None:
        x = 1
        y = 1

        Coordinates(x, y)

    def test_post_init_WHEN_x_is_negative_THEN_raises_invalid_coordinates_exception(self) -> None:
        x = -1
        y = 1

        with self.assertRaises(CoordinatesException):
            Coordinates(x, y)
