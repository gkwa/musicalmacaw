import datetime

from musicalmacaw.parsers.android import AndroidImageParser
from musicalmacaw.parsers.base import TimestampParser
from musicalmacaw.parsers.generic import GenericTimestampParser
from musicalmacaw.parsers.iphone import IPhoneImageParser


def get_default_parsers(timezone: datetime.timezone) -> list[TimestampParser]:
    """Get default list of timestamp parsers."""
    return [
        AndroidImageParser(timezone),
        IPhoneImageParser(timezone),
        GenericTimestampParser(timezone),
    ]


__all__ = [
    "AndroidImageParser",
    "GenericTimestampParser",
    "IPhoneImageParser",
    "TimestampParser",
    "get_default_parsers",
]
