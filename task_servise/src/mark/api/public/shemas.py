from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import datetime, timezone
from typing import List, Optional

from src.mark.domain.entity import Scope

class MarkCreateSchema(BaseModel):
    task_id: int = Field(gt=0)
    quality_score: Scope
    comment: str
    id: int| None = None
    

    

            
