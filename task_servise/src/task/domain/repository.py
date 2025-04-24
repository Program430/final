from abc import ABC, abstractmethod
from typing import List

from src.mark.domain.entity import Mark
from src.task.domain.entity import Task

class TaskDatabaseAbstractRepository(ABC):
    @abstractmethod
    async def create_tasks(tasks: List[Task]) -> List[Task]:
        raise NotImplemented
    
    @abstractmethod
    async def delete_tasks(id: List[int]) -> None:
        raise NotImplemented
    
    @abstractmethod
    async def get_by(**kwargs) -> Task:
        raise NotImplemented
    
    async def get_tasks_for_me(id: int) -> List[Task]:
        raise NotImplemented
    
    async def get_tasks_i_send(id: int) -> List[Task]:
        raise NotImplemented
    
    @abstractmethod
    async def update(task: Task) -> None:
        raise NotImplemented
    
    async def get_all_marks_by_who_take_id(id: int) -> List[Mark]:
        raise NotImplemented



class TaskIntegrationAbstractRepository(ABC):
    """Необходим для интеграции с остальными сервисами"""
    @abstractmethod
    async def get_my_workers(user_id: int) -> List[int]:
        raise NotImplemented