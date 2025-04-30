from enum import IntEnum
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Meeting:
    who_create: int
    name: str
    date: datetime
    description: str
    id: int | None = None