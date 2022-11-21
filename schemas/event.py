from typing import List, Optional
from schemas import CustomBaseModel
from schemas.base.user import UserBase
from schemas.base.attendance import EventAttendeeSchema
from datetime import date, time


class CreateEventSchema(CustomBaseModel):
    date: date
    name: str
    location: str
    description: str
    start_time: time
    end_time: time
    attendee_ids: List[str]
    recurr_until: Optional[date]


class EventSchema(CustomBaseModel):
    pk: str
    date: date
    name: str
    location: str
    description: str
    start_time: time
    end_time: time
    attendee_count: int


class FullEventSchema(EventSchema):
    attendees: List[EventAttendeeSchema]
