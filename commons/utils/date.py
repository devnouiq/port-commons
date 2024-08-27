
from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_datetime_in_est(dt: datetime = None) -> str:
    """
    Convert a datetime to ISO 8601 format in the America/New_York timezone,
    truncated to seconds (no microseconds).

    :param dt: Optional[datetime], the datetime to convert. If None, the current datetime is used.
    :return: str, the datetime in ISO 8601 format truncated to seconds.
    """
    if dt is None:
        dt = datetime.now()

    est_time = dt.astimezone(ZoneInfo("America/New_York"))

    # Truncate to seconds and format as ISO 8601
    return est_time.replace(microsecond=0).isoformat()


def iso_to_naive_datetime(iso_string: str) -> datetime:
    """
    Convert an ISO 8601 formatted string to a naive datetime object (without timezone).
    """
    dt = datetime.fromisoformat(iso_string)
    # Remove timezone information to make it a naive datetime object
    return dt.replace(tzinfo=None)
