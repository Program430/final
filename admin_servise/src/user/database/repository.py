from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload
from typing import Optional, List
from datetime import datetime

from src.authorization.domain.entity import Status

from src.logger import log_errors
from src.database import session_maker
from src.user.domain.entity import User
from src.user.domain.repository import UserDatabaseAbstractRepository
from src.user.database.mapper import UserMapper
from src.user.database.models import UserModel

from src.command.database.mapper import CommandMapper
from src.command.domain.entity import Command

class UserSQLAlchemyRepository(UserDatabaseAbstractRepository):
    @log_errors
    async def create(user: User) -> User:
        async with session_maker() as session:
            user_model = UserMapper.from_entity_to_model(user)
            session.add(user_model)
            await session.commit()
            await session.refresh(user_model)

        return UserMapper.from_model_to_entity(user_model)
    
    @log_errors
    async def get_by(**kwargs) -> Optional[User]:
        async with session_maker() as session:
            query = select(UserModel).filter_by(**kwargs)
            results = await session.execute(query)

            result = results.scalars().first()

        if result is None:
            return None

        return UserMapper.from_model_to_entity(result)
    
    @log_errors
    async def get_user_command(user_id: int) -> Command:
        async with session_maker() as session:
            query = select(UserModel).filter_by(id = user_id).options(joinedload(UserModel.command))
            results = await session.execute(query)

            result = results.scalars().first()

        return CommandMapper.from_model_to_entity(result.command)
    
    @log_errors
    async def update_status(user: User) -> None:
        async with session_maker() as session:
            query = (
                update(UserModel)
                .where(UserModel.id == user.id)
                .values(department_id=user.department, status=user.status, command_id=user.command)
            )
            
            await session.execute(query)
            await session.commit()
    
    @log_errors
    async def delete(ids: List[int]) -> None:
        async with session_maker() as session:
            query = (
                delete(UserModel)
                .where(UserModel.id.in_(ids))
            )
            
            await session.execute(query)
            await session.commit()

    @log_errors
    async def get_my_workers(user: User) -> None:
        async with session_maker() as session:
            if user.status == Status.COMMAND_LIDER or user.status == Status.COMMAND_ADMIN:
                query = (
                    select(UserModel)
                    .where(and_(UserModel.command_id == user.command, UserModel.id != user.id))
                )
            elif user.status == Status.DEPARTMENT_LIDER:
                query = (
                    select(UserModel)
                    .where( and_(
                        UserModel.command_id == user.command,
                        UserModel.department_id == user.department,
                        UserModel.id != user.id
                        ))
                )

            result = await session.execute(query)
            users = result.scalars().all()

            return [UserMapper.from_model_to_entity(user) for user in users]