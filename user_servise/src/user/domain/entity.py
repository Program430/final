from dataclasses import dataclass
from enum import IntEnum

@dataclass
class User:
    login: str
    name: str
    mail: str
    password: str
    id: int | None = None
    deleted_time: str | None = None
    