from enum import IntEnum
from dataclasses import dataclass
from datetime import datetime

class TaskStatus(IntEnum):
    WAITING = 1
    IN_PROCESS = 2
    READY = 3

@dataclass
class Task:
    time_start: datetime
    deadline: datetime
    description: str
    user_who_take: int 
    user_who_send: int 
    name: str
    status: TaskStatus = TaskStatus.WAITING
    id: int | None = None