
from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_datetime_in_est():
    """Get the current datetime in Eastern Standard Time (EST)."""
    return datetime.now(ZoneInfo("America/New_York"))
