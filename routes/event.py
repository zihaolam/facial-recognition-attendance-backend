from datetime import date
from typing import List, Optional
from schemas import BaseQueryParams
from schemas.event import CreateEventSchema, EventSchema, FullEventSchema
from utils.lambda_helpers import lambda_handler
from services.event import Event


class GetEventQueryParams(BaseQueryParams):
    date: Optional[date]


@lambda_handler(body_model=CreateEventSchema, response_model=FullEventSchema)
def create(create_event_body: CreateEventSchema, context):
    new_event = Event.create(create_event_body)
    return new_event


@lambda_handler(response_model=List[EventSchema], query_param_model=GetEventQueryParams)
def find_all(event, context, query_params: GetEventQueryParams):
    return Event.find(date_to_select=query_params.date)


@lambda_handler(response_model=FullEventSchema, path_param_key="id")
def find_one(event, context, event_id):
    return Event.find_one(event_id)
