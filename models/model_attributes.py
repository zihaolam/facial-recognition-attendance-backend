from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from .custom_attributes import DateAttribute, TimeAttribute


class EventModelAttributes:
    description = UnicodeAttribute()
    location = UnicodeAttribute()
    name = UnicodeAttribute()
    date = DateAttribute()
    attendee_count = NumberAttribute()
    start_time = TimeAttribute()
    end_time = TimeAttribute()


class AttendanceModelAttributes:
    timestamp = NumberAttribute()


class UserModelAttributes:
    face_image_path = UnicodeAttribute()
    created_at = NumberAttribute()
    face_id = UnicodeAttribute()
