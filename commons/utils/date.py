from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_datetime_in_est():
    """Get the current datetime in Eastern Standard Time (EST) without timezone info and without microseconds."""
    # Get the current time in EST
    current_time_est = datetime.now(ZoneInfo("America/New_York"))
    # Remove timezone info and microseconds
    naive_datetime_without_microseconds = current_time_est.replace(
        tzinfo=None, microsecond=0)
    return naive_datetime_without_microseconds
