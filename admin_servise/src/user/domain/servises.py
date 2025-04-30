from fastapi import Depends
from typing import List

from src.user.domain.repository import UserDatabaseAbstractRepository
from src.command.domain.repository import CommandDatabaseAbstractRepository
from src.user.database.repository import UserSQLAlchemyRepository
from src.command.database.repository import CommandSQLAlchemyRepository
from src.user.api.schemas import UserAssignSchema
from src.exception import AlreadyExist, PermissionException, DontExist
from src.user.domain.entity import User, Status

from src.authorization.dependences import get_organization_info

class UserServises:
    def __init__(self, user_db_repository: UserDatabaseAbstractRepository, command_db_repository: CommandDatabaseAbstractRepository):
        self.user_db_repository = user_db_repository
        self.command_db_repository = command_db_repository

    async def user_assign(self, user_assign_data: UserAssignSchema, user_organization_info: User = Depends(get_organization_info)) -> None:
        if user_organization_info.status != Status.COMMAND_ADMIN:
            raise PermissionException('Для выполнения этого действия вы должны быть админом команды.')
        
        command = await self.user_db_repository.get_user_command(user_assign_data.id)

        if command.id != user_organization_info.command:
            raise PermissionException('Для выполнения этого действия у вас должна быть одинаковая команда.')

        if user_assign_data.new_status == Status.WORKER or user_assign_data.new_status == Status.DEPARTMENT_LIDER:
            if user_assign_data is None:
                ValueError('Необходимо указать департамент.')

        user = await self.user_db_repository.get_by(id=user_assign_data.id)
        user.status = user_assign_data.new_status
        user.department = user_assign_data.department

        await self.user_db_repository.update(user)
        
    async def get_my_workers(self, user_organization_info: User = Depends(get_organization_info)) -> List[User]:
        if user_organization_info.status == Status.WORKER:
            return []
            
        workers = await self.user_db_repository.get_my_workers(user_organization_info)

        return workers

    # protected
    async def add_user_to_command(self, id: int, code: str) -> None:
        # Автоматическое исключение без проверки
        command = await self.command_db_repository.get_by(code=code)

        user = User(id=id, command=command.id)

        await self.user_db_repository.create(user)

    async def get_user_organization_info(self, id: int) -> User:
        user = await self.user_db_repository.get_by(id=id)

        return user
    
    async def delete_user_from_command(self, id: int) -> None:
        await self.user_db_repository.delete([id])

    async def get_workers_from_my_department_id(self, id: int) -> List[int]:
        user = await self.user_db_repository.get_by(id=id)

        if user.status == Status.WORKER or user.status == Status.DEPARTMENT_LIDER:
            return [i.id for  i in await self.user_db_repository.get_by(id=id)]
        
        return []


user_servise = UserServises(UserSQLAlchemyRepository, CommandSQLAlchemyRepository)