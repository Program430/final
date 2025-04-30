from dataclasses import dataclass
from enum import IntEnum

class Status(IntEnum):
    COMMAND_ADMIN = 1
    COMMAND_LIDER = 2
    DEPARTMENT_LIDER = 3
    WORKER = 4


@dataclass
class UserOrganizationInfo:
    id: int
    command: int
    status: Status
    department: int | None
