from datetime import datetime
from typing import List, Optional
from models import constants
from models.attendance import EventAttendeeModel
from models.helper import add_prefix, add_attributes
from schemas.base.user import UserBase
from utils.lambda_helpers import LambdaException


class Attendance(EventAttendeeModel):
    @staticmethod
    def create(event_id: str, _user: UserBase) -> EventAttendeeModel:
        arrival_time = datetime.now().time()
        try:
            event_attendee: EventAttendeeModel = EventAttendeeModel.get(
                event_id, add_prefix(constants.EVENT, _user.pk))
        except EventAttendeeModel.DoesNotExist as e:
            print(e)
            raise LambdaException(status_code=409, message="Unregistered User")

        event_attendee.arrival_time = arrival_time
        event_attendee.save()

        return event_attendee

    @staticmethod
    def find_by_user_id(user_id: Optional[str] = None, limit=100) -> List[EventAttendeeModel]:
        return list(EventAttendeeModel.event_attendee_user_index.query(add_prefix(constants.EVENT, user_id), limit=100))

    @staticmethod
    def find(limit=100) -> List[EventAttendeeModel]:
        return list(EventAttendeeModel.event_attendee_user_index.scan(limit=limit))
