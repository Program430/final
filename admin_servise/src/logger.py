import logging
import asyncio
from functools import wraps
from typing import Callable, Any

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("../app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_errors(func: Callable) -> Callable:
    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}")
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка в {func.__name__}: {e}")
            raise

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper