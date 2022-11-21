import traceback
from pydantic import BaseModel as PydanticModel
from typing import List, Dict, Union
from pynamodb.models import Model as PynamodbModel
from uuid import uuid4

from utils.lambda_helpers import LambdaException


def add_prefix(*args):
    return '::'.join([str(arg) for arg in args])


def get_pk_metadata(hash_key: str, index: int = 1, prepend="") -> str:
    try:
        return add_prefix(prepend, hash_key.split("::")[index])
    except IndexError as e:
        print("invalid index at", e)
        return ""


def insert_prefix(prefix: str, hash_key: str, depth: int = 1):
    return '::'.join(hash_key.split('::').insert(depth), prefix)


def merge(*models: List[PynamodbModel], **kmodels: Dict[str, Union[List[PynamodbModel], PynamodbModel]]):
    res = {}
    for model in models:
        res.update(model.get_attributes())
    res.update(kmodels)
    return res


def generate_uid():
    return str(uuid4()).replace('-', '')


def add_attributes(source_obj: Union[PydanticModel, PynamodbModel], target_obj: PynamodbModel, exclude=set(), exclude_none=True, additional_attributes: dict = {}):
    target_obj_attr_keys = list(target_obj._get_attributes().keys())

    if isinstance(source_obj, PydanticModel):
        intersected_attrs = {source_attr_key: source_attr_val for source_attr_key, source_attr_val in source_obj.dict(
            exclude=exclude, exclude_none=exclude_none).items() if source_attr_key in target_obj_attr_keys}

        return target_obj._set_attributes(
            **intersected_attrs, **additional_attributes)

    if isinstance(source_obj, PynamodbModel):
        intersected_attrs = {source_attr_key: source_attr_val for source_attr_key,
                             source_attr_val in source_obj.attribute_values.items() if source_attr_key in target_obj_attr_keys}

        intersected_attrs.pop('pk')
        intersected_attrs.pop('sk')
        intersected_attrs.pop("type")

        for attr in exclude:
            intersected_attrs.pop(attr)
        return target_obj._set_attributes(**intersected_attrs, **additional_attributes)

    return LambdaException(status_code=409, message="wrong parameter")
