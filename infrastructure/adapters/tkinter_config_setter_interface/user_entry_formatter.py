from domain.enums import NumberFormatEnum


class UserEntryFormatter:
    __SEPARATOR = NumberFormatEnum.DECIMAL_SEPARATOR.value

    @staticmethod
    def format_as_integer(user_entry: str) -> str:
        if not user_entry:
            return '0'
        return user_entry

    @staticmethod
    def format_as_float(user_entry: str) -> str:
        separator = UserEntryFormatter.__SEPARATOR

        if not user_entry:
            return '0'
        if user_entry.startswith(separator):
            return f'0{user_entry}'
        if user_entry.endswith(separator):
            return user_entry[:-1]
        return user_entry

    @staticmethod
    def format_as_money(user_entry: str) -> str:
        separator = UserEntryFormatter.__SEPARATOR

        if not user_entry:
            return separator.join(['0', '00'])

        if separator not in user_entry:
            user_entry += separator

        integer_part, decimal_part = user_entry.split(separator)

        if not integer_part:
            integer_part = '0'
        decimal_part = decimal_part.ljust(2, '0')

        return separator.join([integer_part, decimal_part])

