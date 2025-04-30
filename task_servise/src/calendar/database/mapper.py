from datetime import datetime

from src.calendar.domain.entity import Meeting
from src.calendar.database.models import MeetingModel

class MeetingMapper:
    @staticmethod
    def to_model(meeting: Meeting) -> MeetingModel:
        return MeetingModel(
            id=meeting.id,
            name=meeting.name,
            date=meeting.date.date() if isinstance(meeting.date, datetime) else meeting.date,
            description=meeting.description,
            who_create=meeting.who_create
        )

    @staticmethod
    def to_entity(meeting_model: MeetingModel) -> Meeting:
        return Meeting(
            id=meeting_model.id,
            name=meeting_model.name,
            date=datetime.combine(meeting_model.date, datetime.min.time()),  # Convert date to datetime
            description=meeting_model.description,
            who_create=meeting_model.who_create
        )