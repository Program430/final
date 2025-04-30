from sqlalchemy import select, update
from typing import Optional, List
from datetime import datetime

from src.logger import log_errors
from src.database import session_maker
from src.command.domain.repository import CommandDatabaseAbstractRepository
from src.command.database.mapper import CommandMapper, DepartmentMapper, MessageMapper
from src.command.database.models import CommandModel, DepartmentModel, MessageModel
from src.command.domain.entity import Command, Department, Message


class CommandSQLAlchemyRepository(CommandDatabaseAbstractRepository):
    @log_errors
    @staticmethod
    async def create(command: Command) -> Command:
        async with session_maker() as session:
            command_model = CommandMapper.from_entity_to_model(command)
            session.add(command_model)
            await session.commit()
            await session.refresh(command_model)

        return CommandMapper.from_model_to_entity(command_model)
    
    @log_errors
    @staticmethod
    async def create_department(department: Department) -> Department:
        async with session_maker() as session:
            department_model = DepartmentMapper.from_entity_to_model(department)
            session.add(department_model)
            await session.commit()
            await session.refresh(department_model)

        return DepartmentMapper.from_model_to_entity(department_model)
    
    @log_errors
    @staticmethod
    async def create_message(message: Message) -> Message:
        async with session_maker() as session:
            message_model = MessageMapper.from_entity_to_model(message)
            session.add(message_model)
            await session.commit()
            await session.refresh(message_model)

        return MessageMapper.from_model_to_entity(message_model)
    
    @log_errors
    @staticmethod
    async def get_by(**kwargs) -> Optional[Command]:
        async with session_maker() as session:
            query = select(CommandModel).filter_by(**kwargs)
            results = await session.execute(query)

            result = results.scalars().first()

        if result is None:
            return None

        return CommandMapper.from_model_to_entity(result)
    
    @log_errors
    @staticmethod
    async def get_department_by(**kwargs) -> Optional[Department]:
        async with session_maker() as session:
            query = select(DepartmentModel).filter_by(**kwargs)
            results = await session.execute(query)

            result = results.scalars().first()

        if result is None:
            return None

        return DepartmentMapper.from_model_to_entity(result)
    
    @log_errors
    @staticmethod
    async def get_messages_by(**kwargs) -> List[Message]:
        async with session_maker() as session:
            query = select(MessageModel).filter_by(**kwargs)
            results = await session.execute(query)

            results = results.scalars().all()

        return [MessageMapper.from_model_to_entity(result) for result in results]
    