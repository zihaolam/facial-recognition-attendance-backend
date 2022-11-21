from schemas import CustomBaseModel
from schemas.base.attendance import AttendanceBase


class CreateAttendanceSchema(CustomBaseModel):
    event_id: str
    face_image: str
