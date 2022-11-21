from models.base import BaseModel
from models.model_attributes import EventModelAttributes
from models.custom_attributes import DateAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute
from . import constants


class EventSortedIndex(GlobalSecondaryIndex):
    class Meta:
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()
    GSI_sort_key = UnicodeAttribute(hash_key=True)
    date = DateAttribute(range_key=True)


class EventModel(BaseModel, EventModelAttributes, discriminator=constants.EVENT):
    GSI_sort_key = UnicodeAttribute(
        default_for_new=constants.EVENT_GSI_SORT_KEY)
    event_sorted_index = EventSortedIndex()
