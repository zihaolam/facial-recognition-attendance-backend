from datetime import date, datetime, timedelta
from typing import List
from models import constants
from models.event import EventModel
from models.attendance import EventAttendeeModel
from models.helper import add_prefix, generate_uid, add_attributes
from models.user import UserModel
from schemas.event import CreateEventSchema, FullEventSchema


class Event(EventModel):
    @staticmethod
    def create(create_event_body: CreateEventSchema) -> FullEventSchema:
        hash_key = create_event_body.name.replace(' ', '_')

        new_events: List[EventModel] = []

        if create_event_body.recurr_until:
            while create_event_body.date <= create_event_body.recurr_until:
                new_event = EventModel(add_prefix(
                    constants.EVENT, hash_key, generate_uid()), constants.DETAIL)
                add_attributes(create_event_body, new_event, exclude={
                               "attendee_ids", "recurr_until"})
                new_events.append(new_event)
                create_event_body.date += timedelta(days=7)

        for _event in new_events:
            _event.attendee_count = len(create_event_body.attendee_ids)

            for _attendee_id in create_event_body.attendee_ids:
                _attendee = UserModel.get(_attendee_id, constants.DETAIL)
                new_event_attendee = EventAttendeeModel(
                    _event.pk, add_prefix(constants.EVENT, _attendee.pk))
                add_attributes(_attendee, new_event_attendee, additional_attributes=dict(
                    date=_event.date))
                new_event_attendee.save()

            _event.save()

        return Event.find_one(new_events[0].pk)

    @staticmethod
    def find_one(event_id) -> FullEventSchema:
        _event_with_details = EventModel.get(event_id, constants.DETAIL)
        _event_with_attendees = list(EventAttendeeModel.query(
            event_id, EventAttendeeModel.sk.startswith(add_prefix(constants.EVENT, constants.USER))))
        return FullEventSchema(
            **_event_with_details.attribute_values, attendees=_event_with_attendees)

    @staticmethod
    def find(last_evaluated_key=None, limit=100, date_to_select: date = None) -> List[EventModel]:
        filters = {}
        if date_to_select is not None:
            filters.update(range_key_condition=(
                EventModel.event_sorted_index.date == date_to_select))
        filters.update(limit=limit)
        if last_evaluated_key is not None:
            filters.update(last_evaluated_key=last_evaluated_key)

        res = EventModel.event_sorted_index.query(
            constants.EVENT_GSI_SORT_KEY, scan_index_forward=False, **filters)

        return list(res)
