from dataclasses import dataclass
from enum import IntEnum

class Status(IntEnum):
    COMMAND_ADMIN = 1
    COMMAND_LIDER = 2
    DEPARTMENT_LIDER = 3
    WORKER = 4


@dataclass
class User:
    status: Status = Status.WORKER
    department: int = None
    command: int = None
    id: int | None = None
    