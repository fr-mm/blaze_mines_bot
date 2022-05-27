from unittest import TestCase

from domain.value_objects import Money, Profit


class TestProfit(TestCase):
    def test_sum_WHEN_money_given_THEN_returns_expected_profit(self) -> None:
        money = Money(3)
        profit = Profit(5)

        result_profit = profit.sum(money)

        expected_profit = Profit(8)
        self.assertEqual(result_profit, expected_profit)

    def test_subtract_WHEN_money_given_THEN_returns_expected_profit(self) -> None:
        money = Money(5)
        profit = Profit(3)

        result_profit = profit.subtract(money)

        expected_profit = Profit(-2)
        self.assertEqual(result_profit, expected_profit)

    def test_to_string_WHEN_value_has_three_digits_THEN_returns_expected_string(self) -> None:
        profit = Profit(123)

        result_string = profit.to_string()

        expected_string = '1,23'
        self.assertEqual(result_string, expected_string)

    def test_to_string_WHEN_value_has_one_digit_THEN_returns_expected_string(self) -> None:
        profit = Profit(1)

        result_string = profit.to_string()

        expected_string = '0,01'
        self.assertEqual(result_string, expected_string)

    def test_to_string_WHEN_value_is_positive_and_has_three_digits_THEN_returns_expected_string(self) -> None:
        profit = Profit(-123)

        result_string = profit.to_string()

        expected_string = '-1,23'
        self.assertEqual(result_string, expected_string)

    def test_to_string_WHEN_value_is_positive_and_has_one_digit_THEN_returns_expected_string(self) -> None:
        profit = Profit(-1)

        result_string = profit.to_string()

        expected_string = '-0,01'
        self.assertEqual(result_string, expected_string)
