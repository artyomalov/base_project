import re

PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def validate_email(value: str | None) -> str | None:
    if value is None:
        return value

    if not isinstance(value, str):
        raise ValueError("Type of input value must be str")

    if not value.strip():
        raise ValueError("Input value must not be empty string")

    if not re.match(pattern=PATTERN, string=value):
        raise ValueError("Email is not valid")

    return value
