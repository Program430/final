from abc import ABC, abstractmethod
from typing import List

from src.comment.domain.entity import Comment

class CommentDatabaseAbstractRepository(ABC):
    @abstractmethod
    async def create_comment(comment: Comment) -> Comment:
        raise NotImplemented
    
    @abstractmethod
    async def get_comments_for_task(task_id: int) -> List[Comment]:
        raise NotImplemented
