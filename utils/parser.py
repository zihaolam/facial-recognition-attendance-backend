import json
from pydantic import ValidationError


def body_parser(event, model=None):
    if model is None:
        return json.loads(event["body"])
    return model(**json.loads(event["body"]))
