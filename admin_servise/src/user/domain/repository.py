from abc import ABC, abstractmethod
from typing import List

from src.authorization.domain.entity import Status
from src.user.domain.entity import User

class UserDatabaseAbstractRepository(ABC):
    @abstractmethod
    async def create(user: User) -> User:
        raise NotImplementedError
    
    async def get_by(**kwargs) -> User:
        raise NotImplementedError
    
    async def update(user: User) -> None:
        raise NotImplementedError
    
    async def get_user_command(user_id: int) -> None:
        raise NotImplementedError
    
    async def delete(user_id: List[int]) -> None:
        raise NotImplementedError
    
    async def get_my_workers(user: User) -> List[User]:
        raise NotImplementedError
    


