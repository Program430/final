from abc import ABC, abstractmethod
from src.user.domain.entity import User

class UserDatabaseAbstractRepository(ABC):
    @abstractmethod
    async def create(user: User) -> User:
        raise NotImplementedError
    
    async def get_by(**kwargs) -> User:
        raise NotImplementedError
    
    async def update(user: User) -> None:
        raise NotImplementedError
    
    async def delete(id: int) -> None:
        raise NotImplementedError
    
    async def undelete(id: int) -> None:
        raise NotImplementedError
    
    async def full_delete() -> None:
        raise NotImplementedError

    
class UserAPIAbstractRepository(ABC):
    @abstractmethod
    async def get_command_by(code: str) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def register_user_to_command(user_id: int, command_code: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_user_from_command(user_id: int) -> None:
        raise NotImplementedError

