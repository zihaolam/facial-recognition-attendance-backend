from datetime import date, time as datetime_time, datetime
from typing import Union
from dateutil.parser import parse
import time


def date_to_timestamp(date: date) -> float:
    return time.mktime(date.timetuple())*1000


def timestamp_to_date(date_timestamp: float) -> Union[date, None]:
    try:
        return datetime.utcfromtimestamp(float(date_timestamp)/1000).date()
    except Exception as e:
        print(e)
        return None


def time_to_str(time_obj: datetime_time) -> str:
    return time_obj.strftime("%H:%M:%S")


def str_to_time(time_string: str) -> datetime_time:
    return datetime_time(*map(int, time_string.split(':')))


def parse_date(string: str) -> Union[datetime, None]:
    try:
        return parse(string)
    except ValueError:
        return None
