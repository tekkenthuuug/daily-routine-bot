from datetime import datetime


def get_timezone_where_time(time: int) -> int:
    utc_now = datetime.utcnow()
    time_delta = time - utc_now.hour
    utc_timezone_offset = time_delta if time_delta <= 12 else time_delta - 24

    return utc_timezone_offset
