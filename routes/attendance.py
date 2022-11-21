from typing import List
from models.constants import DETAIL
from utils.lambda_helpers import lambda_handler
from services.attendance import Attendance
from services.user import User
from schemas.attendance import CreateAttendanceSchema
from schemas.base.attendance import AttendanceBase
from schemas.user import UserBase
from models.user import UserModel
from models.helper import get_pk_metadata
from models import constants


@lambda_handler(body_model=CreateAttendanceSchema, response_model=UserBase)
def create(create_attendance_body: CreateAttendanceSchema, context):
    _user = User.find_by_face(create_attendance_body.face_image)
    new_attendance = Attendance.create(
        create_attendance_body.event_id, _user)
    print(get_pk_metadata(new_attendance.sk, 2, constants.USER))

    return UserModel.get(get_pk_metadata(new_attendance.sk, 2, constants.USER), DETAIL)


@lambda_handler(response_model=List[AttendanceBase])
def find_all(event, context):
    return Attendance.find()
