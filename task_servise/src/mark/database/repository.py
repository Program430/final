from sqlalchemy import select, update
from typing import List, Optional

from src.logger import log_errors
from src.database import session_maker
from src.task.domain.repository import TaskDatabaseAbstractRepository
from src.mark.database.mapper import MarkMapper
from src.mark.domain.entity import Mark
from src.mark.database.models import MarkModel

class MarkSqlAlchemyRepository(TaskDatabaseAbstractRepository):
    @log_errors
    @staticmethod
    async def create_mark(mark: Mark) -> Mark:
        async with session_maker() as session:
            mark_model = MarkMapper.to_model(mark)
            session.add(mark_model)
            await session.commit()
            
            await session.refresh(mark_model)
                
            return MarkMapper.to_entity(mark_model)
        
    @log_errors
    @staticmethod
    async def get_by(**kwargs) -> Optional[Mark]:
        async with session_maker() as session:
            query = select(MarkModel).filter_by(**kwargs)
            results = await session.execute(query)

            result = results.scalars().first()

        if result is None:
            return None

        return MarkMapper.to_entity(result)
    


    
