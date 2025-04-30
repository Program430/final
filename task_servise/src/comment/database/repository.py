from sqlalchemy import select, update
from typing import List, Optional

from src.logger import log_errors
from src.database import session_maker
from src.comment.domain.repository import CommentDatabaseAbstractRepository
from src.comment.database.mapper import CommentMapper
from src.comment.domain.entity import Comment
from src.comment.database.models import CommentModel

class CommentSqlAlchemyRepository(CommentDatabaseAbstractRepository):
    @log_errors
    @staticmethod
    async def create_comment(comment: Comment) -> Comment:
        async with session_maker() as session:
            comment = CommentMapper.to_model(comment)
            session.add_all(comment)
            await session.commit()
            await session.refresh(comment)
                
            return CommentMapper.to_entity(comment)
        
    @log_errors
    @staticmethod
    async def get_comments_for_task(task_id: int) -> List[Comment]:
        async with session_maker() as session:
            query = select(CommentModel).filter_by(task_id = task_id)
            results = await session.execute(query)

            result = results.scalars().all()

            return CommentMapper.to_entity_list(result)


    
