from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import datetime, timezone
from typing import List, Optional

from src.task.domain.entity import TaskStatus

class TaskCreateSchema(BaseModel):
    name: str = Field(max_length=32, description='Название задачи (до 32 символов)')
    description: str = Field(description='Подробное описание задачи')
    deadline: datetime = Field(description='Дата и время выполнения задачи')
    users: Optional[List[int]] = Field(
        None,
        description='ID исполнителей (оставьте None для назначения всем)'
    )

    @field_validator('deadline')
    def validate_deadline(cls, value: datetime) -> datetime:
        if value <= datetime.now(timezone.utc):
            raise ValueError('Дедлайн должен быть в будущем')
        return value

    @field_validator('users')
    def validate_users(cls, users: Optional[List[int]]) -> Optional[List[int]]:
        if users is not None:
            if any(uid <= 0 for uid in users):
                raise ValueError("ID пользователей должны быть > 0")
            if len(users) != len(set(users)):
                raise ValueError("Найдены дубликаты ID пользователей")
        return users
    
class TaskUpdateSchema(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=32, description='Название задачи (до 32 символов)')
    description: str = Field(description='Подробное описание задачи')
    status: TaskStatus = Field(description='WAITING = 1 IN_PROCESS = 2 READY = 3')
    deadline: datetime = Field(description='Дата и время выполнения задачи')

            
