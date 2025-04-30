from sqlalchemy import Column, String, Integer, DateTime, Enum
from src.database import BaseDatabaseModel

class UserModel(BaseDatabaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(40), nullable=False, unique=True)
    name = Column(String(20), nullable=False)
    mail = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    deleted_time = Column(DateTime, nullable=True, default=None)
