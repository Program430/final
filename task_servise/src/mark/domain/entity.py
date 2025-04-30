from enum import IntEnum
from dataclasses import dataclass
from datetime import datetime

class Scope(IntEnum):
    VERY_POOR = 1
    POOR = 2
    AVERAGE = 3
    GOOD = 4
    EXCELLENT = 5

@dataclass
class Mark:
    comment: str
    quality_score: Scope
    task_id: int
    id: int | None = None