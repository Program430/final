from datetime import datetime
from typing import List

from src.calendar.domain.repository import MeetingDatabaseAbstractRepository
from src.task.domain.repository import TaskDatabaseAbstractRepository, TaskIntegrationAbstractRepository
from src.calendar.database.repository import MeetingSqlAlchemyRepository
from src.task.database.repository import TaskSqlAlchemyRepository
from src.task.integration.repository import TaskApiRepository
from src.calendar.api.public.shemas import MeetingCreateSchema, AdUserToMeetingSchema, MeetingUpdateSchema
from src.calendar.domain.entity import Meeting
from src.exception import BadRequest, PermissionException

class MeetingServise:
    def __init__(self, meeting_db_repository: MeetingDatabaseAbstractRepository,
                  task_db_repository: TaskDatabaseAbstractRepository,
                  task_integration_repository: TaskIntegrationAbstractRepository):
        self.meeting_db_repository = meeting_db_repository
        self.task_db_repository = task_db_repository
        self.task_integration_repository = task_integration_repository

    async def create_meeting(self, meeting: MeetingCreateSchema, user_who_send_request_id: int) -> Meeting:
        tasks = await self.task_db_repository.get_tasks_for_me(user_who_send_request_id)

        for task in tasks:
            if task.time_start < meeting < task.deadline:
                raise BadRequest('У вас уже есть задача на этот период.') 
        
        meeting = Meeting(name=meeting.name, description=meeting.description, date=meeting.date)

        meeting = await self.meeting_db_repository.create_meeting(meeting)
            
        await self.meeting_db_repository.add_user(user_who_send_request_id, meeting.id)

        return meeting
    
    async def add_user_to_meeting(self, user_to_add: AdUserToMeetingSchema, user_who_send_request_id: int)-> None:
        workers_id = await self.task_integration_repository.get_my_workers(user_who_send_request_id)

        if not workers_id or user_to_add.user_id not in workers_id:
            BadRequest('У вас нет работников чтобы назначит кому либо встречу. Или это не ваш работник.')

        await self.meeting_db_repository.add_user(user_who_send_request_id, user_to_add.meeting_id)


    async def delete(self, id: int, user_who_send_request_id: int) -> None:
        meeting = await self.meeting_db_repository.get_by(id=id, who_create=user_who_send_request_id)

        if not meeting:
            BadRequest('Встреча не найдена.')

        await self.meeting_db_repository.delete_meeting(id)

    async def update(self, meeting: MeetingUpdateSchema, user_who_send_request_id: int) -> None:
        meeting = await self.meeting_db_repository.get_by(id=id, who_create=user_who_send_request_id)

        if not meeting:
            BadRequest('Встреча не найдена.')

        meeting = Meeting(id = meeting.id, who_create=user_who_send_request_id, )

        await self.meeting_db_repository.update_meeting(id)


meeting_servise = MeetingServise(MeetingSqlAlchemyRepository, TaskSqlAlchemyRepository, TaskApiRepository)

    