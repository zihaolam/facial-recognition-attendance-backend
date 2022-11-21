from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from models.base import BaseModel
from pynamodb.attributes import UnicodeAttribute
from models.helper import add_prefix
from models.model_attributes import UserModelAttributes
from . import constants


class FaceIdIndex(GlobalSecondaryIndex):
    class Meta:
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()
    face_id = UnicodeAttribute(default=0, hash_key=True)


class UserModel(BaseModel, UserModelAttributes, discriminator=constants.USER):
    face_id_index = FaceIdIndex()
