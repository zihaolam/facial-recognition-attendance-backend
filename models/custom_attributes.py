from datetime import date
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

from utils.date_helper import date_to_timestamp, timestamp_to_date, time_to_str, str_to_time


class DateAttribute(NumberAttribute):
    def serialize(self, value: date) -> str:
        return super(NumberAttribute, self).serialize(date_to_timestamp(value))

    def deserialize(self, value: float) -> date:
        return timestamp_to_date(super(NumberAttribute, self).deserialize(value))


class TimeAttribute(UnicodeAttribute):
    def serialize(self, value: date) -> str:
        return super(UnicodeAttribute, self).serialize(time_to_str(value))

    def deserialize(self, value: str) -> date:
        return str_to_time(super(UnicodeAttribute, self).deserialize(value))
