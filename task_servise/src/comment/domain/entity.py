from enum import IntEnum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class TaskStatus(IntEnum):
    WAITING = 1
    IN_PROCESS = 2
    READY = 3

@dataclass
class Comment:
    id: Optional[int] = None
    task_id: int = None
    description: str = None
    created_time: Optional[datetime] = None