

from datetime import timezone, timedelta, datetime


def get_current_datetime_in_est():
    """Get the current datetime in Eastern Standard Time."""
    return datetime.now(timezone(timedelta(hours=-5)))
