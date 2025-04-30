from datetime import datetime
from typing import List

from src.comment.domain.repository import CommentDatabaseAbstractRepository
from src.comment.database.repository import CommentSqlAlchemyRepository
from src.task.domain.repository import TaskDatabaseAbstractRepository
from src.task.database.repository import TaskSqlAlchemyRepository
from src.comment.api.public.shemas import CommentCreateSchema
from src.comment.domain.entity import Comment
from src.exception import BadRequest, PermissionException

class CommentServise:
    def __init__(self, comment_db_repository: CommentDatabaseAbstractRepository, task_db_repository: TaskDatabaseAbstractRepository):
        self.comment_db_repository = comment_db_repository
        self.task_db_repository = task_db_repository

    async def create_comment(self, comment: CommentCreateSchema, user_who_send_request_id: int) -> Comment:
        task = await self.task_db_repository.get_by(id=comment.task_id)

        if not task:
            raise BadRequest('Нет такой задачи.')
        
        if task.user_who_send == user_who_send_request_id or task.user_who_take == user_who_send_request_id:
            return await self.comment_db_repository.create_comment(comment)
        
        raise PermissionError('Задача не принадлежит вам.')
    
    async def get_comments_for_task(self, task_id: int, user_who_send_request_id: int) -> List[Comment]:
        task = await self.task_db_repository.get_by(id=task_id)

        if task.user_who_send != user_who_send_request_id:
            raise PermissionException('Запрещено удалять задачу которую вы не назначали.')

        return await self.task_db_repository.delete_tasks([task_id])
    
comment_servise = CommentServise(CommentSqlAlchemyRepository, TaskSqlAlchemyRepository)

    