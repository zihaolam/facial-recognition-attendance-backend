from typing import Optional
from schemas import CustomBaseModel
from datetime import time, date

from schemas.base.user import UserBase


class AttendanceBase(CustomBaseModel):
    arrival_time: Optional[time]
    pk: str
    sk: str
    face_image_path: str
    date: date


class EventAttendeeWithUserSchema(UserBase):
    arrival_time: Optional[time]
    date: date


class EventAttendeeSchema(AttendanceBase):
    pass
