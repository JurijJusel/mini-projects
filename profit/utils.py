from datetime import datetime, timedelta


def time_stamp() -> int:
    """
    Calculate the Unix timestamp representing the current date and time.
    The time format is: YYYY-MM-DD HH:MM:SS
    Returns:
        int: The current timestamp in seconds.
    """
    dt = datetime.now()
    ts_now = int(datetime.timestamp(dt))
    return ts_now


def time_stamp_minus_one_year() -> int:
    """
    Calculate the Unix timestamp representing the same date and time
    one year ago from the current moment.

    This function uses a 365-day year approximation (does not account for leap years).

    Returns:
        int: The Unix timestamp (in seconds) for the date exactly one year ago.
    """
    dt = datetime.now()
    one_year_ago = dt - timedelta(days=365)
    ts_one_year_ago = int(datetime.timestamp(one_year_ago))
    return ts_one_year_ago
