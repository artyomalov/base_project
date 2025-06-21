VALID_PHONE_NUMBER_SYMBOLS = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "(",
    ")",
    "+",
}


def validate_phone_number(value: str | None) -> str | None:
    """
    Validates phone number and throws
    error if number is not valid.
    Used for pydantic models validation.

    :param value: string than contains only 0-9 numbers, parentheses and plus
    :return: value
    """
    if value is None:
        return value
    if not isinstance(value, str):
        raise ValueError("Type of input value must be str")

    phone_number_set = set(value)
    if not phone_number_set.issubset(VALID_PHONE_NUMBER_SYMBOLS):
        raise ValueError('Phone number must contain 0-9, "(", ")", "+" symbols')

    return value
