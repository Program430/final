from sqlalchemy import select, update, delete
from typing import List, Optional

from src.logger import log_errors
from src.database import session_maker
from src.calendar.domain.repository import MeetingDatabaseAbstractRepository
from src.calendar.database.mapper import MeetingMapper
from src.calendar.domain.entity import Meeting
from src.calendar.database.models import MeetingModel, UserIdModel

class MeetingSqlAlchemyRepository(MeetingDatabaseAbstractRepository):
    @log_errors
    async def create_meeting(meeting: Meeting) -> Meeting:
        async with session_maker() as session:
            meeting = MeetingMapper.to_model(meeting)
            session.add(meeting)
    
            await session.commit()
            await session.refresh(meeting)
                
            return MeetingMapper.to_entity(meeting)
        
    @log_errors
    async def get_by(**kwargs) -> Optional[Meeting]:
        async with session_maker() as session:
            query = select(MeetingModel).filter_by(**kwargs)
            results = await session.execute(query)

            result = results.scalars().first()

        if result is None:
            return None

        return MeetingMapper.to_entity(result)
    
    @log_errors
    async def add_user(user_id: int, meeting_id: int) -> None:
        async with session_maker() as session:
            user = UserIdModel(user_id=user_id, meeting_id=meeting_id)

            session.add(user)

            await session.commit()
    
    @log_errors
    async def delete_meeting(meeting_id: int) -> None:
        async with session_maker() as session:
            query = delete(MeetingModel).where(MeetingModel.id == meeting_id)
            
            await session.execute(query)
                
            await session.commit()

    @log_errors
    async def update_meeting(meeting: Meeting) -> None:
        async with session_maker() as session:
            query = (
                update(MeetingModel)
                .where(MeetingModel.id == meeting.id)
                .values(date = meeting.date, description = meeting.description, 
                        name = meeting.name)
            )
            
            await session.execute(query)
            await session.commit()
    

    
