from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_datetime_in_est():
    """Get the current datetime in Eastern Standard Time (EST) without timezone info."""
    # Get the current time in EST
    current_time_est = datetime.now(ZoneInfo("America/New_York"))
    # Return a naive datetime by stripping the timezone info
    return current_time_est.replace(tzinfo=None)
