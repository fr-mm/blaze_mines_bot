from unittest import TestCase

from mockito import mock

from domain.aggregates import ScreenRegionAggregate
from domain.value_objects import ScreenRegion


class TestScreenRegionAggregate(TestCase):
    def setUp(self) -> None:
        self.screen_region = mock(ScreenRegion)

    def test_start_game_WHEN_screen_region_given_THEN_stores_screen_region(self) -> None:
        screen_region_aggregate = ScreenRegionAggregate()

        screen_region_aggregate.set_start_game(self.screen_region)
        stored_location = screen_region_aggregate.start_game

        self.assertEqual(stored_location, self.screen_region)

    def test_withdraw_money_WHEN_screen_region_given_THEN_stores_screen_region(self) -> None:
        screen_region_aggregate = ScreenRegionAggregate()

        screen_region_aggregate.set_withdraw_money(self.screen_region)
        stored_location = screen_region_aggregate.withdraw_money

        self.assertEqual(stored_location, self.screen_region)

    def test_bet_field_WHEN_screen_region_given_THEN_stores_screen_region(self) -> None:
        screen_region_aggregate = ScreenRegionAggregate()

        screen_region_aggregate.set_bet_field(self.screen_region)
        stored_location = screen_region_aggregate.bet_field

        self.assertEqual(stored_location, self.screen_region)

    def test_square_WHEN_screen_region_given_THEN_stores_screen_region(self) -> None:
        screen_region_aggregate = ScreenRegionAggregate()

        screen_region_aggregate.set_square(self.screen_region)
        stored_location = screen_region_aggregate.square

        self.assertEqual(stored_location, self.screen_region)
