import datetime
import re

from musicalmacaw.parsers.base import TimestampParser


class IPhoneImageParser(TimestampParser):
    """Parser for iPhone image format: IMG_YYYY-MM-DD_HH-MM-SS.jpg"""

    def __init__(self, timezone: datetime.timezone = datetime.UTC) -> None:
        self.pattern: re.Pattern[str] = re.compile(
            r"IMG_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})"
        )
        self.timezone = timezone

    def parse(self, filename: str) -> datetime.datetime | None:
        match = self.pattern.search(filename)
        if not match:
            return None

        year, month, day, hour, minute, second = match.groups()
        try:
            return datetime.datetime(
                int(year),
                int(month),
                int(day),
                int(hour),
                int(minute),
                int(second),
                tzinfo=self.timezone,
            )
        except ValueError:
            return None
