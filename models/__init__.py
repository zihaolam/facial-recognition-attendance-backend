from .attendance import EventAttendeeModel
from .event import EventModel
from .user import UserModel


class FinalModel(EventAttendeeModel, EventModel, UserModel):
    pass


def run():
    if not FinalModel.exists():
        FinalModel.create_table(read_capacity_units=25,
                                write_capacity_units=25)


run()
