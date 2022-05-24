from domain.enums import NumberFormatEnum


def validate_float(entry: str) -> bool:
    separator = NumberFormatEnum.DECIMAL_SEPARATOR.value
    if not entry[-1].isdigit() and entry[-1] != separator:
        return False
    if entry.count(separator) > 1:
        return False
    return True
