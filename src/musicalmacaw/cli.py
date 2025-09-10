import argparse
import logging
import pathlib
import sys

from musicalmacaw.calculator import DurationCalculator
from musicalmacaw.logging_config import setup_logging
from musicalmacaw.parsers import get_default_parsers
from musicalmacaw.timezone_detection import get_current_timezone_info
from musicalmacaw.timezone_utils import parse_timezone


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    # Get system timezone info for help text
    _, tz_description = get_current_timezone_info()

    parser = argparse.ArgumentParser(
        description="Show duration from image creation time till now",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("filepath", help="Path to image file")

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (use -v, -vv, or -vvv)",
    )

    parser.add_argument(
        "-t",
        "--timezone",
        default=None,
        help=(
            f"Timezone for timestamps (e.g., UTC, +0800, -0500). "
            f"Default: system timezone ({tz_description})"
        ),
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI application."""
    args = parse_arguments()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Check if file exists
    if not pathlib.Path(args.filepath).exists():
        logger.error("File does not exist: %s", args.filepath)
        sys.exit(1)

    # Determine timezone to use
    if args.timezone is not None:
        # User provided explicit timezone
        try:
            timezone = parse_timezone(args.timezone)
            logger.debug("Using user-specified timezone: %s", timezone)
        except Exception:
            logger.exception("Invalid timezone")
            sys.exit(1)
    else:
        # Use system timezone
        timezone, tz_description = get_current_timezone_info()
        logger.debug(
            "Using detected system timezone: %s (%s)", timezone, tz_description
        )

    # Initialize calculator with default parsers
    parsers = get_default_parsers(timezone)
    calculator = DurationCalculator(parsers, timezone)

    # Calculate duration
    duration = calculator.calculate_duration(args.filepath)

    if duration is None:
        logger.error("Could not extract timestamp from filename or file metadata")
        sys.exit(1)

    # Output result (silence is golden - only output the result)
    sys.stdout.write(duration + "\n")
    sys.exit(0)  # Explicit success exit code
