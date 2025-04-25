from abc import ABC, abstractmethod
import aiohttp
from typing import List

from src.config import ADMIN_SERVISE_ADRESS, SECRET_KEY_BETWEEN_SERVISES
from src.mark.domain.repository import MarkIntegrationAbstractRepository
from src.common.token import generate_access_tokens

class MarkApiRepository(MarkIntegrationAbstractRepository):
    headers = {
        'accept': 'application/json'
    }
    @classmethod
    async def workers_from_my_department(cls, user_id: int) -> List[int]:
        cls.headers['secret-key'] = SECRET_KEY_BETWEEN_SERVISES
        async with aiohttp.ClientSession() as session:
            address = f'{ADMIN_SERVISE_ADRESS}/protected/user/get_workers_from_my_department_id'
            async with session.post(
                address,
                headers=cls.headers,
                json={'id': user_id},
                timeout=5
            ) as response:
                if response.status == 200:
                    workers_data = await response.json()
                    return [worker for worker in workers_data]
                response.raise_for_status()
            