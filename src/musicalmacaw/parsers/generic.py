import datetime
import re

from musicalmacaw.parsers.base import TimestampParser


class GenericTimestampParser(TimestampParser):
    """Parser for generic timestamp format: YYYY-MM-DD_HH-MM-SS or YYYYMMDD_HHMMSS"""

    def __init__(self, timezone: datetime.timezone = datetime.UTC) -> None:
        self.patterns: list[re.Pattern[str]] = [
            re.compile(r"(\d{4})-(\d{2})-(\d{2})[_-](\d{2})-(\d{2})-(\d{2})"),
            re.compile(r"(\d{8})[_-](\d{6})"),
        ]
        self.timezone = timezone

    def parse(self, filename: str) -> datetime.datetime | None:
        # Try first pattern: YYYY-MM-DD_HH-MM-SS
        match = self.patterns[0].search(filename)
        if match:
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
                pass

        # Try second pattern: YYYYMMDD_HHMMSS
        match = self.patterns[1].search(filename)
        if not match:
            return None

        date_str, time_str = match.groups()
        try:
            return datetime.datetime.strptime(
                f"{date_str}_{time_str}", "%Y%m%d_%H%M%S"
            ).replace(tzinfo=self.timezone)
        except ValueError:
            return None
