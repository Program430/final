from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional
    

class CommandCreateSchema(BaseModel):
    name: str = Field(min_length=4, max_length=100, examples=["command123"])
    description: str