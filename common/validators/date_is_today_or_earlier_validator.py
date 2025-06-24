from datetime import datetime, UTC


def validate_date_is_today_or_earlier(value: datetime) -> datetime | None:
    current_datetime = datetime.now(UTC)
    if value is None:
        return value
    # datetime_from_value = datetime.fromisoformat(value)
    if value > current_datetime:
        raise ValueError(
            "Provided date and time are later \
        the current date and time"
        )
    return value
