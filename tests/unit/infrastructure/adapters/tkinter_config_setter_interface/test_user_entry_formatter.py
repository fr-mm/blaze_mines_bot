from unittest import TestCase

from infrastructure.adapters.tkinter_config_setter_interface.user_entry_formatter import UserEntryFormatter


class TestUserEntryFormatter(TestCase):
    def test_format_as_integer_WHEN_user_input_is_not_empty_THEN_returns_unchanged_user_input(self) -> None:
        user_input = '1'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_integer(user_input)

        expected_result = user_input
        self.assertEqual(result, expected_result)

    def test_format_as_integer_WHEN_user_input_is_empty_THEN_returns_zero(self) -> None:
        user_input = ''
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_integer(user_input)

        expected_result = '0'
        self.assertEqual(result, expected_result)

    def test_format_as_float_WHEN_user_input_format_is_ok_THEN_return_unchanged_user_input(self) -> None:
        user_input = '1.50'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_float(user_input)

        expected_result = user_input
        self.assertEqual(result, expected_result)

    def test_format_as_float_WHEN_user_input_starts_with_comma_THEN_adds_zero_at_the_start(self) -> None:
        user_input = '.50'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_float(user_input)

        expected_result = '0.50'
        self.assertEqual(result, expected_result)

    def test_format_as_float_WHEN_user_input_ends_with_comma_THEN_removes_comma(self) -> None:
        user_input = '50.'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_float(user_input)

        expected_result = '50'
        self.assertEqual(result, expected_result)

    def test_format_as_float_WHEN_user_input_is_empty_THEN_returns_zero(self) -> None:
        user_input = ''
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_float(user_input)

        expected_result = '0'
        self.assertEqual(result, expected_result)

    def test_format_as_money_WHEN_user_input_format_is_ok_THEN_returns_unchanged_user_input(self) -> None:
        user_input = '1.50'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_money(user_input)

        expected_result = user_input
        self.assertEqual(result, expected_result)

    def test_format_as_money_WHEN_user_input_starts_with_comma_THEN_adds_zero_at_the_start(self) -> None:
        user_input = '.50'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_money(user_input)

        expected_result = '0.50'
        self.assertEqual(result, expected_result)

    def test_format_as_money_WHEN_user_input_has_no_comma_THEN_adds_comma_and_two_zeros_at_the_end(self) -> None:
        user_input = '50'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_money(user_input)

        expected_result = '50.00'
        self.assertEqual(result, expected_result)

    def test_format_as_money_WHEN_user_input_ends_with_comma_THEN_adds_two_zeros_at_the_end(self) -> None:
        user_input = '5.'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_money(user_input)

        expected_result = '5.00'
        self.assertEqual(result, expected_result)

    def test_format_as_money_WHEN_user_input_has_one_digit_after_the_comma_THEN_adds_one_zero_at_the_end(self) -> None:
        user_input = '5.3'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_money(user_input)

        expected_result = '5.30'
        self.assertEqual(result, expected_result)

    def test_format_as_money_WHEN_user_input_starts_with_comma_and_has_one_digit_after_THEN_adds_one_zero_at_the_start_and_one_at_the_end(self) -> None:
        user_input = '.3'
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_money(user_input)

        expected_result = '0.30'
        self.assertEqual(result, expected_result)

    def test_format_as_money_WHEN_user_input_is_empty_THEN_returns_formatted_zero(self) -> None:
        user_input = ''
        user_entry_formatter = UserEntryFormatter()

        result = user_entry_formatter.format_as_money(user_input)

        expected_result = '0.00'
        self.assertEqual(result, expected_result)
