from datetime import datetime
from typing import List

from src.task.domain.repository import TaskDatabaseAbstractRepository, TaskIntegrationAbstractRepository
from src.task.database.repository import TaskSqlAlchemyRepository
from src.task.integration.repository import TaskApiRepository
from src.task.api.public.shemas import TaskCreateSchema, TaskUpdateSchema
from src.task.domain.entity import Task
from src.exception import BadRequest, PermissionException

class TaskServise:
    def __init__(self, task_db_repository: TaskDatabaseAbstractRepository,
                  task_integration_repository: TaskIntegrationAbstractRepository):
        self.task_db_repository = task_db_repository
        self.task_integration_repository = task_integration_repository

    async def create_task(self, task: TaskCreateSchema, user_who_send_request_id: int) -> List[Task]:
        workers_list = await self.task_integration_repository.get_my_workers(user_who_send_request_id)

        if not workers_list:
            raise BadRequest('У вас нет работников.')
        
        users_list = []
        if not task.users:
            users_list = workers_list
        else:
            users_list = [i for i in task.users if i in workers_list]

        tasks = [Task(name=task.name, 
                      user_who_send = user_who_send_request_id, 
                      user_who_take=i,
                      deadline = task.deadline,
                      description=task.description,
                      time_start=datetime.now()) for i in users_list]

        return await self.task_db_repository.create_tasks(tasks)

    async def delete_task(self, task_id: int, user_who_send_request_id: int) -> None:
        task = await self.task_db_repository.get_by(id=task_id)

        if task.user_who_send != user_who_send_request_id:
            raise PermissionException('Запрещено удалять задачу которую вы не назначали.')

        return await self.task_db_repository.delete_tasks([task_id])
    
    async def get_tasks_for_me(self, user_who_send_request_id: int) -> List[Task]:
        return await self.task_db_repository.get_by(user_who_take=user_who_send_request_id)
    
    async def get_tasks_i_send(self, user_who_send_request_id: int) -> List[Task]:
        return await self.task_db_repository.get_by(user_who_send=user_who_send_request_id)
    
    async def update_task(self, task_to_update: TaskUpdateSchema, user_who_send_request_id: int) -> List[Task]:
        task = await self.task_db_repository.get_by(id=task_to_update.id, user_who_send=user_who_send_request_id)

        if not task:
            BadRequest('Задача с таким айди не найтена либо принадлежит не вам.')

        task.name = task_to_update.name
        task.description = task_to_update.description
        task.status = task_to_update.status
        task.deadline = task_to_update.deadline

        return await self.task_db_repository.update(task)


task_servise = TaskServise(TaskSqlAlchemyRepository, TaskApiRepository)

    