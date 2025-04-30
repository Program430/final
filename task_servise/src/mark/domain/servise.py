from datetime import datetime
from typing import List

from src.mark.domain.repository import MarkDatabaseAbstractRepository, MarkIntegrationAbstractRepository
from src.task.domain.repository import TaskDatabaseAbstractRepository
from src.mark.database.repository import MarkSqlAlchemyRepository
from src.task.database.repository import TaskSqlAlchemyRepository
from src.mark.integration.repository import MarkApiRepository
from src.mark.api.public.shemas import MarkCreateSchema
from src.mark.domain.entity import Mark
from src.exception import BadRequest, PermissionException

class MarkServise:
    def __init__(self, mark_db_repository: MarkDatabaseAbstractRepository,
                  mark_integration_repository: MarkIntegrationAbstractRepository,
                  task_db_repository: TaskDatabaseAbstractRepository):
        self.mark_db_repository = mark_db_repository
        self.mark_integration_repository = mark_integration_repository
        self.task_db_repository = task_db_repository

    async def create_mark(self, mark: MarkCreateSchema, user_who_send_request_id: int) -> Mark:
        task = await self.task_db_repository.get_by(id = mark.task_id, user_who_send = user_who_send_request_id)

        if not task:
            raise BadRequest('Задача не найдена либо пренадлежит не вам.')
        
        mark = Mark(comment = mark.comment, task_id=mark.task_id, quality_score=mark.quality_score)

        mark = await self.mark_db_repository.create_mark(mark)

        return mark
    
    async def get_my_marks(self, user_who_send_request_id: int) -> List[Mark]:
        my_tasks = self.task_db_repository.get_tasks_for_me(user_who_send_request_id)
        marks = []
        for i in my_tasks:
            marks.append(await self.mark_db_repository.get_by(task_id = i.id))

        return marks

    async def help_to_count_average_mark(self, id: int) -> float:
        avg = await self.task_db_repository.get_all_marks_by_who_take_id(id)

        sum = 0
        counter = len(avg)

        if not counter:
            return 0

        for i in avg:
            sum += i.quality_score
        
        return sum/counter
            

    async def get_average_marks_result(self, user_who_send_request_id: float) -> float:
        user_ids = await self.mark_integration_repository.workers_from_my_department(user_who_send_request_id)

        user_average_mark = await self.help_to_count_average_mark(user_who_send_request_id)

        if not user_average_mark:
            raise BadRequest('У вас нет ни одной оценки.')
        
        sum = 0
        counter = len(user_ids)
        for i in user_ids:
            sum += await self.help_to_count_average_mark(user_who_send_request_id)

        return sum/counter

        

mark_servise = MarkServise(MarkSqlAlchemyRepository, MarkApiRepository, TaskSqlAlchemyRepository)

    