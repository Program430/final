import aiohttp
from src.logger import log_errors
import logging
from typing import List

from src.user.domain.repository import UserAPIAbstractRepository
from src.config import SECRET_KEY_BETWEEN_SERVISES, ADMIN_SERVISE_ADRESS
from src.user.domain.exception import AnotherMicroserviseError

class UserAPIRepository(UserAPIAbstractRepository):
    headers = {'secret-key': SECRET_KEY_BETWEEN_SERVISES,
               'Content-Type': 'application/json',
               'accept': 'application/json'}
    
    @classmethod
    @log_errors
    async def get_command_by(cls, code: str) -> int:
        async with aiohttp.ClientSession() as session:
            address = f'{ADMIN_SERVISE_ADRESS}/protected/command/get_command_by_code'
            async with session.post(
                address,
                headers=cls.headers,
                data=f'"{code}"',
                timeout=5
            ) as response:
                if response.status == 200:
                    return int(await response.text())
                response.raise_for_status()

    @classmethod
    @log_errors
    async def register_user_to_command(cls, user_id: int, code: str) -> None:
        async with aiohttp.ClientSession() as session:
            address = f'{ADMIN_SERVISE_ADRESS}/protected/user/add_user_to_command'
            async with session.post(
                address,
                headers=cls.headers,
                json={'code': code, 'id': user_id},
                timeout=5
            ) as response:
                if response.status == 204:
                    return
                response.raise_for_status()
                raise AnotherMicroserviseError(f'Ошибка регистрации: {response.status}')

    @classmethod
    async def delete_user_from_command(cls, user_id: int) -> None:
        async with aiohttp.ClientSession() as session:
            address = f'{ADMIN_SERVISE_ADRESS}/protected/user/delete_users_from_command'
            async with session.post(
                address,
                headers=cls.headers,
                json={'id': user_id},
                timeout=5
            ) as response:
                if response.status == 204:
                    return
                response.raise_for_status()