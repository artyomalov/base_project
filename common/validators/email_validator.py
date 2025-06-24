def validate_email(value: str | None) -> str | None:
    if value is None:
        return value
    if not isinstance(value, str):
        raise ValueError("Type of input value must be str")
    if "@" not in value:
        raise ValueError('Email must contain "@"')
    return value
