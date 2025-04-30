from abc import ABC, abstractmethod
from typing import List

from src.command.domain.entity import Command, Department, Message

class CommandDatabaseAbstractRepository(ABC):
    @abstractmethod
    async def create(command: Command) -> Command:
        raise NotImplementedError
    
    async def create_department(department: Department) -> Department:
        raise NotImplementedError
    
    async def create_message(massage: Message) -> Message:
        raise NotImplementedError
    
    async def get_by(**kwargs) -> Command:
        raise NotImplementedError
    
    async def get_department_by(**kwargs) -> Department:
        raise NotImplementedError
    
    async def get_messages_by(**kwargs) -> List[Message]:
        raise NotImplementedError
    

