from unittest import TestCase

import mouse
from mockito import when, unstub, verify, mock

from domain.value_objects import Coordinates, ScreenRegion
from infrastructure.adapters import MouseClickerAdapter


class TestMouseClickerAdapter(TestCase):
    def tearDown(self) -> None:
        unstub()

    def test_click_on_coordinates_WHEN_coordinates_given_THEN_move_mouse_to_coordinates(self) -> None:
        coordinates = Coordinates(x=100, y=200)
        when(mouse).move(x=100, y=200)
        when(mouse).click()
        clicker = MouseClickerAdapter()

        clicker.click_on_coordinates(coordinates)

        verify(mouse).move(x=100, y=200)

    def test_click_on_coordinates_WHEN_coordinates_given_THEN_click_after_moving(self) -> None:
        moved_event = 'moved'
        clicked_event = 'clicked'
        ordered_events = []
        coordinates = Coordinates(x=100, y=200)
        when(mouse).move(..., ...).thenReturn(ordered_events.append(moved_event))
        when(mouse).click().thenReturn(ordered_events.append(clicked_event))
        clicker = MouseClickerAdapter()

        clicker.click_on_coordinates(coordinates)

        expected_ordered_events = [moved_event, clicked_event]
        self.assertEqual(ordered_events, expected_ordered_events)

    def test_click_on_screen_region_WHEN_given_screen_region_THEN_calls_click_on_coordinates_of_center_screen_region(self) -> None:
        screen_region = ScreenRegion(
            top_left=Coordinates(x=200, y=400),
            bottom_right=Coordinates(x=600, y=700)
        )
        center_coordinates = Coordinates(x=400, y=550)
        when(MouseClickerAdapter).click_on_coordinates(center_coordinates)
        clicker = MouseClickerAdapter()

        clicker.click_on_screen_region(screen_region)

        verify(MouseClickerAdapter).click_on_coordinates(center_coordinates)
