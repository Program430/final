from abc import ABC, abstractmethod
import aiohttp

from src.config import ADMIN_SERVISE_ADRESS
from src.task.domain.repository import TaskIntegrationAbstractRepository
from src.common.token import generate_access_tokens

class TaskApiRepository(TaskIntegrationAbstractRepository):
    url = f'{ADMIN_SERVISE_ADRESS}/user/get_my_workers'
    headers = {
        'accept': 'application/json'
    }
    @classmethod
    async def get_my_workers(cls, user_id: int):
        cls.headers['authorization_token'] = f'Bearer {generate_access_tokens(user_id)}'
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.url, headers=cls.headers) as response:
                workers_data = await response.json()
                return [worker['id'] for worker in workers_data]