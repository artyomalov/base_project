def validate_string_is_not_empty(value: str | None) -> str | None:
    """
    Checks if value without whitespaces
    is not empty.
    """
    if value is None:
        return value
    if not len(value.strip()):
        raise ValueError("Input can't be empty")
    return value
