import dataclasses
import datetime


@dataclasses.dataclass
class TimestampParser:
    """Base class for timestamp parsers using dependency injection pattern."""

    def parse(self, filename: str) -> datetime.datetime | None:
        """Parse timestamp from filename. Return None if no match."""
        raise NotImplementedError
