from fastapi import Depends

from src.user.domain.repository import UserDatabaseAbstractRepository, UserAPIAbstractRepository
from src.user.database.repository import UserSQLAlchemyRepository
from src.user.outside_api.repository import UserAPIRepository
from src.user.api.schemas import UserCreateSchema, UserLoginSchema, UserUpdateSchema
from src.user.domain.exception import AlreadyExist, PermissionException, DontExist, AnotherMicroserviseError
from src.user.domain.entity import User

from src.authorization.domain.entity import UserOrganizationInfo
from src.authorization.domain.entity import Status
from src.authorization.dependences import get_user_organization_info

class UserServises:
    def __init__(self, user_db_repository: UserDatabaseAbstractRepository, user_api_repository: UserAPIAbstractRepository):
        self.user_db_repository = user_db_repository
        self.user_api_repository = user_api_repository

    async def _is_user_command_admin(self, user_who_send_request: UserOrganizationInfo, id: int) -> bool:
        return (user_who_send_request.status == Status.COMMAND_ADMIN
                and user_who_send_request.status == (await get_user_organization_info(id)).command)

    async def _user_data_already_exist_check(self, login: str, mail: str) -> None:
        user = await self.user_db_repository.get_by(login=login)

        if user:
            raise AlreadyExist('Пользователь с таким логином уже существует.')
        
        user= await self.user_db_repository.get_by(mail=mail)

        if user:
            raise AlreadyExist('Пользователь с такой почтой уже существует.')
        
    async def _user_data_not_exist_check(self, id: int, login: str, mail: str) -> None:
        user_to_update = await self.user_db_repository.get_by(id=id)

        if not user_to_update:
            raise DontExist('Пользователя с таким айди не существует')

        user = await self.user_db_repository.get_by(login=login)

        if user and user.login != user_to_update.login:
            raise AlreadyExist('Пользователь с таким логином уже существует.')
        
        user = await self.user_db_repository.get_by(mail=mail)

        if user and user.mail != user_to_update.mail:
            raise AlreadyExist('Пользователь с такой почтой уже существует.')
        
    async def user_create(self, potencial_user_data: UserCreateSchema, code: str) -> User:
        if potencial_user_data.command_code is None and code is None:
            raise ValueError('Укажите код команды.')
        
        # если код указан в 2х местах тогда берется из тела запроса
        if potencial_user_data.command_code:
            code = potencial_user_data.command_code

        command = await self.user_api_repository.get_command_by(code)

        if not command:
            raise DontExist('Команды с таким кодом приглашения не существует.')

        print('Прошло')

        await self._user_data_already_exist_check(potencial_user_data.login, potencial_user_data.mail)
        
        user = User(
            login=potencial_user_data.login,
            name=potencial_user_data.name,
            mail=potencial_user_data.mail,
            password=potencial_user_data.password,
        )

        # Вообще желательно сделать это в одной транзакции
        user = await self.user_db_repository.create(user)
        await self.user_api_repository.register_user_to_command(user.id, code)
        
        return user

    async def user_login(self, user_login_data: UserLoginSchema) -> User:
        user = await self.user_db_repository.get_by(login=user_login_data.login, password=user_login_data.password)

        if not user:
            raise DontExist('Возможно вы ошиблись в логине или пароле.')
        
        return user
    
    async def user_update(self, user_who_send_request: UserOrganizationInfo, user_update_data: UserUpdateSchema) -> None:
        user = User(
                id=user_update_data.id,
                login=user_update_data.login,
                name=user_update_data.name,
                mail=user_update_data.mail,
                password=user_update_data.password,
            )


        if (await self._is_user_command_admin(user_who_send_request, user.id)) or user_who_send_request.id == user.id:

            user_who_send_request.id == user.id

            await self._user_data_not_exist_check(user.id, user.login, user.mail)

            await self.user_db_repository.update(user)

        else:
            raise PermissionException('Вы должны быть админом одной с пользователем команды.')
        
    async def user_delete(self, user_who_send_request: UserOrganizationInfo, id: int) -> None:
        if user_who_send_request.id == id:
            await self.user_api_repository.delete_user_from_command(id)
            return await self.user_db_repository.delete(id)
        
        raise PermissionException('Только сам пользователь может удалить себя.')
    
    async def user_undelete(self, user_who_send_request: UserOrganizationInfo, id: int) -> None:
        if user_who_send_request.id == id:
            return await self.user_db_repository.undelete(id)
        
        raise PermissionException('Только сам пользователь может воcстановить себя.')


user_servise = UserServises(UserSQLAlchemyRepository, UserAPIRepository)