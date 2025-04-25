from fastapi import Depends
from typing import List

from src.command.api.schemas import CommandCreateSchema
from src.command.domain.repository import CommandDatabaseAbstractRepository
from src.user.domain.repository import UserDatabaseAbstractRepository
from src.command.database.repository import CommandSQLAlchemyRepository
from src.user.database.repository import UserSQLAlchemyRepository
from src.exception import AlreadyExist, PermissionException, DontExist
from src.command.domain.entity import Command, Department, Message
from src.user.domain.entity import User
from src.authorization.domain.entity import Status

class CommandServises:
    def __init__(self, command_db_repository: CommandDatabaseAbstractRepository, user_db_repository: UserDatabaseAbstractRepository):
        self.command_db_repository = command_db_repository
        self.user_db_repository = user_db_repository
    
    async def command_create(self, user_organization_info: User, potencial_command_data: CommandCreateSchema) -> Command:
        if user_organization_info.status != Status.COMMAND_ADMIN:
            raise PermissionException('Для выполнения этого действия вы должны быть админом команды.')
        
        command = await self.command_db_repository.get_by(name=potencial_command_data.name)

        if command:
            raise AlreadyExist('Команда с таким именем уже существует.')

        command = Command(name=potencial_command_data.name, description=potencial_command_data.description)

        command = await self.command_db_repository.create(command)

        user_organization_info.command = command.id

        await self.user_db_repository.update(user_organization_info)

        return command

    async def department_create(self, user_organization_info: User, department_name: str) -> Department:
        
        if user_organization_info.status != Status.COMMAND_ADMIN:
            raise PermissionException('Для выполнения этого действия вы должны быть админом команды.')
        
        department = await self.command_db_repository.get_department_by(name=department_name, command_id=user_organization_info.command)

        if department:
            raise AlreadyExist('Департамент с таким именем уже существует.')

        department = Department(name=department_name, command=user_organization_info.command)

        department = await self.command_db_repository.create_department(department)

        return department
    
    async def message_create(self, user_organization_info: User, message_name: str, message_information: str) -> Message:
        
        if not (user_organization_info.status == Status.COMMAND_ADMIN or user_organization_info.status == Status.COMMAND_LIDER):
            raise PermissionException('Для выполнения этого действия вы должны быть админом или лидером команды.')
        
        message = Message(name = message_name, info = message_information)

        message = await self.command_db_repository.create_message(message)

        return message
    
    async def messages_get(self, user_organization_info: User) -> List[Message]:
        
        messages = await self.command_db_repository.get_messages_by(command_id=user_organization_info.command)

        return messages
    
    # protected

    async def get_command_by_code(self, code: str) -> Command:
        command = await self.command_db_repository.get_by(code=code)
        
        if not command:
            raise DontExist('Команды с таким кодом не существует.')
        
        return command
 

command_servise = CommandServises(CommandSQLAlchemyRepository, UserSQLAlchemyRepository)