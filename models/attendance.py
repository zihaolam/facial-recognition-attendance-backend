from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from models.base import BaseModel
from pynamodb.attributes import NumberAttribute
from .model_attributes import UserModelAttributes
from .custom_attributes import DateAttribute, TimeAttribute
from . import constants


class EventAttendeeUserIndex(GlobalSecondaryIndex):
    class Meta:
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()
    sk = UnicodeAttribute(hash_key=True)
    date = DateAttribute(range_key=True)


class EventAttendeeModel(BaseModel, UserModelAttributes, discriminator=constants.ATTENDANCE):
    arrival_time = TimeAttribute(null=True)
    event_attendee_user_index = EventAttendeeUserIndex()
    date = DateAttribute()
