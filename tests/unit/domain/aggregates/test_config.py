from unittest import TestCase

from domain.aggregates import Config
from domain.value_objects import Seconds, Money, MartingaleMultiplier, MaxMartingales


class TestConfig(TestCase):
    def test_init_WHEN_no_args_given_THEN_returns_instance_with_default_values(self) -> None:
        Config()

    def test_seconds_between_actions_getter_WHEN_value_given_THEN_returns_seconds_with_given_value(self) -> None:
        seconds_between_actions_value = 2
        config = Config(seconds_between_actions=seconds_between_actions_value)

        returned_seconds = config.seconds_between_actions

        expected_seconds = Seconds(seconds_between_actions_value)
        self.assertEqual(returned_seconds, expected_seconds)

    def test_starting_bet_getter_WHEN_value_given_THEN_returns_money_with_given_value(self) -> None:
        starting_bet_value = 10
        config = Config(starting_bet=starting_bet_value)

        returned_money = config.starting_bet

        expected_money = Money(starting_bet_value)
        self.assertEqual(returned_money, expected_money)

    def test_martingale_multiplier_getter_WHEN_value_given_THEN_returns_martingale_multiplier_with_given_value(self) -> None:
        martingale_multiplier_value = 2
        config = Config(martingale_multiplier=martingale_multiplier_value)

        returned_martingale_multiplier = config.martingale_multiplier

        expected_martingale_multiplier = MartingaleMultiplier(martingale_multiplier_value)
        self.assertEqual(returned_martingale_multiplier, expected_martingale_multiplier)

    def test_max_martingales_getter_WHEN_value_given_THEN_returns_max_martingales_with_given_value(self) -> None:
        max_martingales_value = 4
        config = Config(max_martingales=max_martingales_value)

        returned_max_martingales = config.max_martingales

        expected_max_martingales = MaxMartingales(max_martingales_value)
        self.assertEqual(returned_max_martingales, expected_max_martingales)

    def test_reset_after_max_martingales_getter_WHEN_value_given_THEN_returns_given_value(self) -> None:
        reset_after_max_martingales_value = False
        config = Config(reset_after_max_martingales=reset_after_max_martingales_value)

        returned_reset_after_max_martingales = config.reset_after_max_martingales

        expected_reset_after_max_martingales = reset_after_max_martingales_value
        self.assertEqual(returned_reset_after_max_martingales, expected_reset_after_max_martingales)

    def test_seconds_between_actions_setter_WHEN_valid_value_given_THEN_sets_seconds_with_given_value(self) -> None:
        config = Config()
        seconds_between_actions_value = 10

        config.seconds_between_actions = seconds_between_actions_value

        expected_seconds_between_actions = Seconds(seconds_between_actions_value)
        self.assertEqual(config.seconds_between_actions, expected_seconds_between_actions)

    def test_starting_bet_setter_WHEN_valid_input_string_given_THEN_sets_starting_bet_with_given_parsed_value(self) -> None:
        config = Config()
        starting_bet_input_string = '2,50'

        config.starting_bet = starting_bet_input_string

        expected_starting_bet = Money(250)
        self.assertEqual(config.starting_bet, expected_starting_bet)

    def test_martingale_multiplier_setter_WHEN_valid_value_given_THEN_sets_martingale_multiplier_with_given_value(self) -> None:
        config = Config()
        martingale_multiplier_value = 3

        config.martingale_multiplier = martingale_multiplier_value

        expected_martingale_multiplier = MartingaleMultiplier(martingale_multiplier_value)
        self.assertEqual(config.martingale_multiplier, expected_martingale_multiplier)

    def test_max_martingales_setter_WHEN_valid_value_given_THEN_sets_max_martingales_with_given_value(self) -> None:
        config = Config()
        max_martingales_value = 6

        config.max_martingales = max_martingales_value

        expected_max_martingales = MaxMartingales(max_martingales_value)
        self.assertEqual(config.max_martingales, expected_max_martingales)

    def test_reset_after_max_martingales_setter_WHEN_value_given_THEN_sets_reset_after_max_martingales_with_given_value(self) -> None:
        config = Config()
        reset_after_max_martingales = False

        config.reset_after_max_martingales = reset_after_max_martingales

        self.assertEqual(config.reset_after_max_martingales, reset_after_max_martingales)
