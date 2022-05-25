class UserEntryFormatter:
    COMMA = ','

    @staticmethod
    def format_as_integer(user_entry: str) -> str:
        if not user_entry:
            return '0'
        return user_entry

    @staticmethod
    def format_as_float(user_entry: str) -> str:
        comma = UserEntryFormatter.COMMA

        if not user_entry:
            return '0'
        if user_entry.startswith(comma):
            return f'0{user_entry}'
        if user_entry.endswith(comma):
            return user_entry[:-1]
        return user_entry

    @staticmethod
    def format_as_money(user_entry: str) -> str:
        comma = UserEntryFormatter.COMMA

        if not user_entry:
            return '0,00'

        if comma not in user_entry:
            user_entry += comma

        integer_part, decimal_part = user_entry.split(comma)

        if not integer_part:
            integer_part = '0'
        decimal_part = decimal_part.ljust(2, '0')

        return comma.join([integer_part, decimal_part])

