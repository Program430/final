from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import datetime, timezone
from typing import List, Optional

from src.task.domain.entity import TaskStatus

class MeetingCreateSchema(BaseModel):
    name: int = Field(gt=0)
    description: str = Field(description='Подробное описание задачи')
    date: datetime

class AdUserToMeetingSchema(BaseModel):
    meeting_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
