import json
import traceback
from typing import List, Union
from schemas import ApiResponse, DefaultResponseData, ErrorResponse
from pydantic import ValidationError, parse_obj_as


class LambdaException(Exception):
    message: str
    status_code: int

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def lambda_handler(body_model=None, response_model=None, path_param_key=None, query_param_model=None):
    def wrapper(handler):
        def inner(event, context):
            try:
                args = []
                args.append(body_model(
                    **json.loads(event["body"])) if body_model is not None else event)

                args.append(context)

                if path_param_key is not None:
                    try:
                        args.append(event["pathParameters"][path_param_key])
                    except KeyError:
                        raise LambdaException(
                            status_code=422, message=f"{path_param_key} is invalid")

                kwargs = {}
                if query_param_model is not None:
                    query_parameters = event["queryStringParameters"]
                    if query_parameters is None:
                        query_parameters = {}

                    try:
                        kwargs.update(query_params=query_param_model(
                            **query_parameters))

                    except KeyError:
                        raise LambdaException(
                            status_code=422, message="Invalid query string parameters")
                res = handler(*args, **kwargs)

                if response_model is None:
                    return lambda_response(data=res)

                return lambda_response(model=response_model, data=res)

            except KeyError as e:
                traceback.print_exc()
                return lambda_response(status_code=422, message=f"Error, required path parameter: {path_param_key} not found")
            except ValidationError as e:
                traceback.print_exc()
                return lambda_response(status_code=422, message=e.json())
            except LambdaException as e:
                traceback.print_exc()
                return lambda_response(status_code=e.status_code, message=e.message)
            except Exception as e:
                traceback.print_exc()
                return lambda_response(status_code=500, message="Server Error")
        return inner
    return wrapper


def response_body_parser(data, model=None):
    if model is None:
        return data

    if isinstance(data, (List, list)):
        return [obj.dict(by_alias=True) for obj in parse_obj_as(model, data)]

    return parse_obj_as(model, data).dict(by_alias=True)


def lambda_response(model=DefaultResponseData, status_code=200, data: Union[dict, str] = {}, message="Success"):
    if status_code >= 400:
        return ErrorResponse(body=message.json() if not isinstance(message, str) else dict(message=message), statusCode=status_code).json()
    return ApiResponse(
        message=message, statusCode=status_code, body=response_body_parser(data, model)).json()
