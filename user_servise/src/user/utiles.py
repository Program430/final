import asyncio
from src.user.database.repository import UserSQLAlchemyRepository
from src.user.outside_api.repository import UserAPIRepository

async def users_delete_loop():
    await asyncio.sleep(60 * 5 * 60 * 24)
    # сделал как быстрее, проблема множества запросов 
    for i in await UserSQLAlchemyRepository.full_delete():
        await UserAPIRepository.delete_user_from_command(i)