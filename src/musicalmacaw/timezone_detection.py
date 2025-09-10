import datetime
import logging
import time


def _validate_timezone_name() -> None:
    """Validate that timezone name is available."""
    msg = "No timezone name available"
    if not (hasattr(time, "tzname") and time.tzname[0]):
        raise ValueError(msg)


def _validate_timezone_offset(hours_offset: int) -> None:
    """Validate that timezone offset is non-zero."""
    msg = "No timezone offset detected"
    if hours_offset == 0:
        raise ValueError(msg)


def _try_get_timezone_from_time_module() -> datetime.timezone | None:
    """Try to get timezone using time module."""
    try:
        _validate_timezone_name()

        # Get UTC offset in seconds
        utc_offset_seconds = -time.timezone
        if time.daylight and time.tzname[1]:
            # Adjust for daylight saving time if active
            utc_offset_seconds = -time.altzone

        offset = datetime.timedelta(seconds=utc_offset_seconds)
        return datetime.timezone(offset, time.tzname[0])
    except (AttributeError, OSError, ValueError):
        return None


def _try_get_timezone_from_time_offset() -> datetime.timezone | None:
    """Try to get timezone using time.timezone offset."""
    try:
        # Use time.timezone which gives UTC offset in seconds
        if not hasattr(time, "timezone"):
            return None

        utc_offset_seconds = -time.timezone
        if time.daylight and hasattr(time, "altzone"):
            # Use daylight saving time offset if available
            utc_offset_seconds = -time.altzone

        # Convert to hours for validation
        hours_offset = utc_offset_seconds // 3600
        _validate_timezone_offset(hours_offset)

        offset = datetime.timedelta(seconds=utc_offset_seconds)
        return datetime.timezone(offset)
    except (AttributeError, OSError, ValueError):
        return None


def get_system_timezone() -> datetime.timezone:
    """Get the system timezone."""
    logger = logging.getLogger(__name__)

    # Try to get the system timezone using time.tzname and time.timezone
    timezone = _try_get_timezone_from_time_module()
    if timezone is not None:
        logger.debug("Detected system timezone: %s", timezone)
        return timezone

    logger.debug("Could not detect system timezone using time module")

    # Alternative method: use time.timezone offset directly
    timezone = _try_get_timezone_from_time_offset()
    if timezone is not None:
        logger.debug("Detected system timezone via time offset: %s", timezone)
        return timezone

    logger.debug("Could not detect system timezone using time offset")

    # Fallback to UTC
    logger.debug("Falling back to UTC timezone")
    return datetime.UTC


def get_current_timezone_info() -> tuple[datetime.timezone, str]:
    """Get current timezone and a human-readable description."""
    timezone = get_system_timezone()

    # Handle UTC case early
    if timezone == datetime.UTC:
        return timezone, "UTC"

    # Handle timezone with offset
    offset = timezone.utcoffset(None)
    if offset is None:
        return timezone, "Unknown"

    total_seconds = int(offset.total_seconds())
    hours = total_seconds // 3600
    minutes = abs(total_seconds % 3600) // 60

    # Format based on whether minutes are present
    if minutes == 0:
        description = f"+{hours:02d}00" if hours >= 0 else f"{hours:03d}00"
    else:
        description = (
            f"+{hours:02d}{minutes:02d}" if hours >= 0 else f"{hours:03d}{minutes:02d}"
        )

    return timezone, description
