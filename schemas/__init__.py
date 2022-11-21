from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, parse_obj_as
from pydantic.generics import GenericModel
from utils.to_camel import to_camel


class CustomBaseModel(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
        validate_assignment = True
        arbitrary_types_allowed = True


class CustomGenericModel(GenericModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
        validate_assignment = True


class Keys:
    hash_key = None
    range_key = None

    def __init__(self, hash_key, range_key=None):
        self.hash_key = hash_key
        self.range_key = range_key


class DefaultResponseData(CustomBaseModel):
    pass


class ErrorResponseBody(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    body: ErrorResponseBody
    statusCode: int


class ApiResponse(CustomBaseModel):
    message: str
    body: Any
    statusCode: int


class BaseQueryParams(CustomBaseModel):
    step: Optional[str]
    limit: Optional[int]


def path_params_factory(param_types: Dict[str, Any]):
    class PathParameters(CustomBaseModel):
        def __init__(self):
            for key, val in param_types.items():
                setattr(self, key, val)

    return PathParameters()
