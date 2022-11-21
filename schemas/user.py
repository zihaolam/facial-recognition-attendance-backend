from typing import List
from schemas import CustomBaseModel, Keys
from schemas.base.attendance import EventAttendeeSchema
from schemas.base.user import UserBase


class CreateUserSchema(CustomBaseModel):
    face_image: str
    full_name: str

    def build_keys(self) -> Keys:
        return Keys(self.full_name)


class CreateMultipleUserSchema(CustomBaseModel):
    face_images: List[CreateUserSchema]


class FullUserSchema(UserBase):
    attendances: List[EventAttendeeSchema]
