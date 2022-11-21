from schemas import CustomBaseModel
from datetime import date, time


class EventBase(CustomBaseModel):
    pk: str
    date: date
    name: str
    location: str
    description: str
    start_time: time
    end_time: time
    attendee_count: int
