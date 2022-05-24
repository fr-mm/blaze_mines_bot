from unittest import TestCase

from domain.exceptions import MoneyException
from domain.value_objects import Money, MartingaleMultiplier


class TestMoney(TestCase):
    def test_init_WHEN_valid_value_THEN_creates_instance(self) -> None:
        value = 1

        Money(value)

    def test_post_init_WHEN_value_is_less_than_min_THEN_raises_money_exception(self) -> None:
        value = 0

        with self.assertRaises(MoneyException):
            Money(value)

    def test_sum_WHEN_money_given_THEN_returns_new_money_with_expected_summed_value(self) -> None:
        first_value = 2
        second_value = 5
        first_money = Money(first_value)
        second_money = Money(second_value)

        result_money = first_money.sum(second_money)

        expected_money = Money(7)
        self.assertEqual(result_money, expected_money)

    def test_multiply_WHEN_martingale_multiplier_given_THEN_returns_expected_money(self) -> None:
        martingale_multiplier = MartingaleMultiplier(2)
        starting_money = Money(5)

        result_money = starting_money.multiply(martingale_multiplier)

        expected_money = Money(10)
        self.assertEqual(result_money, expected_money)

    def test_to_string_WHEN_value_is_four_digits_long_THEN_returns_expected_string(self) -> None:
        value = 1234
        money = Money(value)

        result_string = money.to_string()

        expected_string = '12,34'
        self.assertEqual(result_string, expected_string)

    def test_to_string_WHEN_value_is_one_digit_long_THEN_returns_expected_string(self) -> None:
        value = 5
        money = Money(value)

        result_string = money.to_string()

        expected_string = '0,05'
        self.assertEqual(result_string, expected_string)

    def test_from_string_WHEN_valid_input_THEN_returns_expected_money(self) -> None:
        input_string = '0,05'

        result_money = Money.from_string(input_string)

        expected_money = Money(5)
        self.assertEqual(result_money, expected_money)

    def test_from_string_WHEN_input_has_invalid_char_THEN_raises_money_exception(self) -> None:
        input_string = '0,u5'

        with self.assertRaises(MoneyException):
            Money.from_string(input_string)

    def test_from_string_WHEN_input_is_3_chars_long_THEN_raises_money_exception(self) -> None:
        input_string = '0,5'

        with self.assertRaises(MoneyException):
            Money.from_string(input_string)

    def test_from_string_WHEN_input_has_two_commas_THEN_raises_money_exception(self) -> None:
        input_string = '0,0,5'

        with self.assertRaises(MoneyException):
            Money.from_string(input_string)

    def test_from_string_WHEN_input_has_comma_at_wrong_index_THEN_raises_money_exception(self) -> None:
        input_string = '00,5'

        with self.assertRaises(MoneyException):
            Money.from_string(input_string)
