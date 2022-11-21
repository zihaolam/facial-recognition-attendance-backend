from schemas import CustomBaseModel


class UserBase(CustomBaseModel):
    face_image_path: str
    face_id: str
    pk: str  # student_id
    created_at: float
    sk: str
