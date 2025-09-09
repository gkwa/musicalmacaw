import datetime
import logging
import pathlib

from musicalmacaw.parsers.base import TimestampParser


class DurationCalculator:
    """Calculate and format duration between timestamps."""

    def __init__(
        self,
        parsers: list[TimestampParser],
        current_timezone: datetime.timezone = datetime.UTC,
    ) -> None:
        self.parsers = parsers
        self.current_timezone = current_timezone
        self.logger = logging.getLogger(__name__)

    def parse_timestamp(self, filepath: str) -> datetime.datetime | None:
        """Try to parse timestamp using available parsers."""
        filename = pathlib.Path(filepath).name
        self.logger.debug("Parsing filename: %s", filename)

        for parser in self.parsers:
            self.logger.debug("Trying parser: %s", parser.__class__.__name__)
            timestamp = parser.parse(filename)
            if not timestamp:
                continue

            self.logger.info(
                "Successfully parsed timestamp: %s using %s",
                timestamp,
                parser.__class__.__name__,
            )
            return timestamp

        self.logger.warning("No parser could extract timestamp from: %s", filename)
        return None

    def format_duration(self, start_time: datetime.datetime) -> str:
        """Format duration from start_time to now in user-friendly format."""
        now = datetime.datetime.now(tz=self.current_timezone)
        duration = now - start_time

        total_seconds = int(duration.total_seconds())
        if total_seconds < 0:
            return "0m"  # Future timestamp

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        parts: list[str] = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")

        return "".join(parts) if parts else "0m"

    def calculate_duration(self, filepath: str) -> str | None:
        """Calculate duration from file timestamp to now."""
        timestamp = self.parse_timestamp(filepath)
        if not timestamp:
            return None

        return self.format_duration(timestamp)
