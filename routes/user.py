from typing import List
from utils.lambda_helpers import lambda_handler
from services.user import User
from schemas.user import CreateMultipleUserSchema, FullUserSchema
from schemas.base.user import UserBase


@lambda_handler(body_model=CreateMultipleUserSchema, response_model=List[UserBase])
def create(create_user_body: CreateMultipleUserSchema, context):
    new_users = [User.create(_user) for _user in create_user_body.face_images]
    return new_users


@lambda_handler(response_model=List[UserBase])
def find_all(event, context):
    return User.find()


@lambda_handler(response_model=FullUserSchema, path_param_key='id')
def find_one(event, context, user_id: str):
    return User.find_by_id(user_id)
