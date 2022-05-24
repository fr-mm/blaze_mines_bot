from domain.enums import NumberFormatEnum


def validate_money(entry: str) -> bool:
    separator = NumberFormatEnum.DECIMAL_SEPARATOR.value
    if not entry[-1].isdigit() and entry[-1] != separator:
        return False
    if entry.count(separator) > 1:
        return False
    if separator in entry and len(entry.split(separator)[-1]) > 2:
        return False
    return True
