
from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_datetime_in_est() -> str:
    """Return the current datetime in ISO 8601 format in the America/New_York timezone."""
    return datetime.now(ZoneInfo("America/New_York")).isoformat())
