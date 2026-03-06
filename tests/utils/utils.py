import random
from datetime import datetime, timedelta

def random_datetime_between(start: datetime, end: datetime) -> str:
    if end < start:
        start, end = end, start
    delta_seconds = int((end - start).total_seconds())
    result_date = start + timedelta(seconds=random.randint(0, delta_seconds))
    return result_date.isoformat(timespec="seconds")

def date_to_iso(date: datetime) -> str:
    return date.isoformat(timespec="seconds")