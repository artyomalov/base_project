def check_string_is_not_empty(string: str) -> bool:
    """
    Checks if string without whitespaces
    is not empty.
    """
    if string is None:
        raise ValueError("Input string cannot be None")
    return bool(string.strip())
