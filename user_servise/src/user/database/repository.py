from sqlalchemy import select, update, delete, and_
from typing import Optional, List
from datetime import datetime, timedelta

from src.logger import log_errors
from src.database import session_maker
from src.user.domain.entity import User
from src.user.domain.repository import UserDatabaseAbstractRepository
from src.user.database.mapper import UserMapper
from src.user.database.models import UserModel


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
    async def update(user: User) -> None:
        async with session_maker() as session:
            query = (
                update(UserModel)
                .where(UserModel.id == user.id)
                .values(login=user.login, name=user.name, password=user.password, mail=user.mail)
            )
            
            await session.execute(query)
            await session.commit()

    @log_errors
    async def delete(id: int) -> None:
        async with session_maker() as session:
            query = (
                update(UserModel)
                .where(UserModel.id == id)
                .values(deleted_time = datetime.utcnow())
            )
            
            await session.execute(query)
            await session.commit()
    
    @log_errors
    async def undelete(id: int) -> None:
        async with session_maker() as session:
            query = (
                update(UserModel)
                .where(UserModel.id == id)
                .values(deleted_time = None)
            )
            
            await session.execute(query)
            await session.commit()

    @log_errors
    async def full_delete() -> List[int]:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        async with session_maker() as session:
            query = select(UserModel.id).where(
                and_(
                    UserModel.deleted_time.is_not(None),
                    UserModel.deleted_time < thirty_days_ago
                )
            )

            results = await session.execute(query)
            user_ids = results.scalars().all()

            if not user_ids:
                return []

            query = delete(UserModel).where(UserModel.id.in_(user_ids))

            await session.execute(query)

            await session.commit()

            return user_ids
    