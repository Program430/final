import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logging.info("Подключение к базе по адресу: " + DATABASE_URL)

engine = create_async_engine(DATABASE_URL)

session_maker = async_sessionmaker(engine, class_=AsyncSession)

BaseDatabaseModel = declarative_base()
