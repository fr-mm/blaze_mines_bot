from unittest import TestCase

from domain.exceptions import InvalidCoordinatesException
from domain.value_objects import Coordinates


class TestCoordinates(TestCase):
    def test_post_init_WHEN_x_is_negative_THEN_raises_invalid_coordinates_exception(self) -> None:
        x = -1
        y = 1

        with self.assertRaises(InvalidCoordinatesException):
            Coordinates(x, y)
