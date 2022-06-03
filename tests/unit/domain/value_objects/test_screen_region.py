from unittest import TestCase

from domain.exceptions import ScreenRegionException
from domain.value_objects import Coordinates
from domain.value_objects.screen_region import ScreenRegion


class TestScreenRegion(TestCase):
    def test_init_WHEN_coordinates_are_valid_THEN_creates_instance(self) -> None:
        top_left = Coordinates(1, 1)
        bottom_right = Coordinates(10, 10)

        ScreenRegion(top_left=top_left, bottom_right=bottom_right)

    def test_post_init_WHEN_top_left_x_is_bigger_than_bottom_right_x_THEN_raises_invalid_screen_region_exception(self) -> None:
        top_left = Coordinates(10, 1)
        bottom_right = Coordinates(1, 10)

        with self.assertRaises(ScreenRegionException):
            ScreenRegion(top_left=top_left, bottom_right=bottom_right)

    def test_get_full_screen_WHEN_called_THEN_returns_screen_region_with_width_greater_than_height(self) -> None:
        screen_region = ScreenRegion.full_screen()

        self.assertGreater(screen_region.bottom_right.x, screen_region.bottom_right.y)
