import datetime
import re

from musicalmacaw.parsers.base import TimestampParser


class AndroidImageParser(TimestampParser):
    """Parser for Android image format: IMG_YYYYMMDD_HHMMSS.jpg"""

    def __init__(self, timezone: datetime.timezone = datetime.UTC) -> None:
        self.pattern: re.Pattern[str] = re.compile(r"IMG_(\d{8})_(\d{6})")
        self.timezone = timezone

    def parse(self, filename: str) -> datetime.datetime | None:
        match = self.pattern.search(filename)
        if not match:
            return None

        date_str, time_str = match.groups()
        try:
            return datetime.datetime.strptime(
                f"{date_str}_{time_str}", "%Y%m%d_%H%M%S"
            ).replace(tzinfo=self.timezone)
        except ValueError:
            return None
