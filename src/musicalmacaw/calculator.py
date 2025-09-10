import datetime
import logging
import pathlib

from musicalmacaw.parsers.base import TimestampParser

# Maximum days to show hours alongside days for readability
MAX_DAYS_WITH_HOURS = 7


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

    def _get_file_mtime(self, filepath: str) -> datetime.datetime | None:
        """Get file modification time as fallback timestamp."""
        path = pathlib.Path(filepath)
        if not path.exists():
            return None

        try:
            # Get modification time as timestamp
            mtime = path.stat().st_mtime
            # Convert to datetime in the current timezone
            file_time = datetime.datetime.fromtimestamp(mtime, tz=self.current_timezone)
        except (OSError, ValueError) as e:
            self.logger.debug("Could not get file modification time: %s", e)
            return None

        self.logger.info("Using file modification time: %s", file_time)
        return file_time

    def parse_timestamp(self, filepath: str) -> datetime.datetime | None:
        """Try to parse timestamp using available parsers, fallback to file mtime."""
        filename = pathlib.Path(filepath).name
        self.logger.debug("Parsing filename: %s", filename)

        # Try filename parsing first
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

        self.logger.info(
            "No parser could extract timestamp from filename: %s", filename
        )

        # Fallback to file modification time
        self.logger.info("Falling back to file modification time")
        return self._get_file_mtime(filepath)

    def format_duration(self, start_time: datetime.datetime) -> str:
        """Format duration from start_time to now in user-friendly format."""
        now = datetime.datetime.now(tz=self.current_timezone)
        duration = now - start_time

        total_seconds = int(duration.total_seconds())
        if total_seconds < 0:
            return "0m"  # Future timestamp

        days = total_seconds // 86400  # 24 * 60 * 60
        remaining_seconds = total_seconds % 86400
        hours = remaining_seconds // 3600
        minutes = (remaining_seconds % 3600) // 60

        parts: list[str] = []

        # Use days if >= 1 day
        if days > 0:
            parts.append(f"{days}d")
            # Only show hours for shorter periods to avoid verbose output
            if days < MAX_DAYS_WITH_HOURS and hours > 0:
                parts.append(f"{hours}h")
        else:
            # Less than a day - show hours and minutes as before
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
