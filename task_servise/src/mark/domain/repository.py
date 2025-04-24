from abc import ABC, abstractmethod
from typing import List

from src.mark.domain.entity import Mark

class MarkDatabaseAbstractRepository(ABC):
    @abstractmethod
    async def create_mark(mark: Mark) -> Mark:
        raise NotImplemented
    
    @abstractmethod
    async def get_by(**kwargs) -> Mark:
        raise NotImplemented
    

class MarkIntegrationAbstractRepository(ABC):
    """Необходим для интеграции с остальными сервисами"""
    @abstractmethod
    async def workers_from_my_department(user_id: int) -> List[int]:
        raise NotImplemented