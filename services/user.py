from datetime import datetime
from typing import List
from models.helper import add_prefix
from models.user import UserModel
from schemas.user import CreateUserSchema, FullUserSchema
from services.attendance import Attendance
from utils.lambda_helpers import LambdaException
from utils.s3_helper import S3, BucketNames
from datauri import InvalidDataURI
from utils.facial_recognition import amazon_rekognition
from models import constants


class User(UserModel):
    @staticmethod
    def create(create_user_body: CreateUserSchema) -> UserModel:
        keys = create_user_body.build_keys()
        hash_key = add_prefix(constants.USER, keys.hash_key)
        new_user = UserModel(hash_key, constants.DETAIL)

        s3 = S3(BucketNames.USER_BUCKET)

        try:
            url = s3.upload(create_user_body.face_image)

        except InvalidDataURI as e:
            raise LambdaException(status_code=422, message="Invalid data uri")

        new_user.face_image_path = url
        new_user.face_id = amazon_rekognition.add_face(
            create_user_body.face_image)
        new_user.created_at = datetime.now().timestamp()*1000
        new_user.save()

        return new_user

    @staticmethod
    def find(last_evaluated_key=None, limit=100) -> List[UserModel]:
        filters = dict(limit=limit)
        if last_evaluated_key is not None:
            filters["last_evaluated_key"] = last_evaluated_key

        res = UserModel.scan(
            **filters)

        return list(res)

    @staticmethod
    def find_by_id(user_id: str) -> FullUserSchema:
        _user_with_details = UserModel.get(user_id, constants.DETAIL)
        _user_attendances = Attendance.find_by_user_id(user_id)
        return FullUserSchema(**_user_with_details.attribute_values, attendances=_user_attendances)

    @staticmethod
    def find_by_face(face_image: str) -> UserModel:
        face_id = amazon_rekognition.detect_face(face_image)
        if face_id is None:
            raise LambdaException(status_code=409, message="Face not found")

        _users: List[UserModel] = list(
            UserModel.face_id_index.query(face_id, limit=1))

        if len(_users) == 0:
            raise LambdaException(status_code=409, message="Face not found")

        return _users[0]
