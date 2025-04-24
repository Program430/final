from dataclasses import dataclass
from enum import IntEnum

@dataclass
class Command:
    name: str
    description: str
    code: str | None = None
    id: int | None = None
    

@dataclass
class Department:
    name: str
    command: int |None = None
    id: int | None = None

@dataclass
class Message:
    command: int
    info: str
    name: str
    date: str | None = None
    id: int | None = None