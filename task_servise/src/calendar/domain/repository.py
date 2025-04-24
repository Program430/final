from abc import ABC, abstractmethod
from typing import List, Optional

from src.calendar.domain.entity import Meeting

class MeetingDatabaseAbstractRepository(ABC):
    @abstractmethod
    async def create_meeting(meeting: Meeting) -> Meeting:
        raise NotImplemented
    
    @abstractmethod
    async def get_by(**kwargs) -> Optional[Meeting]:
        raise NotImplemented
    
    @abstractmethod
    async def delete_meeting(meeting_id: int) -> None:
        raise NotImplemented
    
    @abstractmethod
    async def update_meeting(meeting: Meeting) -> None:
        raise NotImplemented
    
    @abstractmethod
    async def is_user_meeting(user_id: int, meeting_id: int) -> bool:
        raise NotImplemented
    