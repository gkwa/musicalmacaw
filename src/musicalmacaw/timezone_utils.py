import datetime

# Minimum length for timezone string with minutes
MIN_TIMEZONE_LENGTH_WITH_MINUTES = 5


def parse_timezone(timezone_str: str) -> datetime.timezone:
    """Parse timezone string into timezone object."""
    if not timezone_str:
        return datetime.UTC

    timezone_str = timezone_str.upper()

    # Handle common timezone abbreviations
    timezone_map = {
        "UTC": datetime.UTC,
        "GMT": datetime.UTC,
    }

    if timezone_str in timezone_map:
        return timezone_map[timezone_str]

    # Handle offset format like +0800, -0500
    if not timezone_str.startswith(("+", "-")):
        # If we can't parse it, default to UTC
        return datetime.UTC

    try:
        sign = 1 if timezone_str[0] == "+" else -1
        hours = int(timezone_str[1:3])
        minutes = (
            int(timezone_str[3:5])
            if len(timezone_str) >= MIN_TIMEZONE_LENGTH_WITH_MINUTES
            else 0
        )
        offset = datetime.timedelta(hours=sign * hours, minutes=sign * minutes)
        return datetime.timezone(offset)
    except (ValueError, IndexError):
        # If we can't parse it, default to UTC
        return datetime.UTC
