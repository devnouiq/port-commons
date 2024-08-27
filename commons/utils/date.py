
from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_datetime_in_est() -> str:
    """Return the current datetime in ISO 8601 format in the America/New_York timezone."""
    return datetime.now(ZoneInfo("America/New_York")).isoformat()


def iso_to_datetime(iso_string: str) -> datetime:
    """
    Convert an ISO 8601 formatted string to a datetime object.
    """
    return datetime.fromisoformat(iso_string)
