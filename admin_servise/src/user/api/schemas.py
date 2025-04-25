from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional

from src.authorization.domain.entity import Status

class UserAssignSchema(BaseModel):
    id: int
    new_status: Optional[Status] = None
    department: Optional[int] = None
 

class MyWorkersResponseSchema(BaseModel):
    id: int
    status: Status
    department: int | None