from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from src.user.domain.entity import Status
from src.database import BaseDatabaseModel

class CommandModel(BaseDatabaseModel):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    code = Column(String(32), nullable=False, default=lambda: uuid4().hex[:32])

    departments = relationship('DepartmentModel', back_populates='command')
    users = relationship('UserModel', back_populates='command')
    messages = relationship('MessageModel', back_populates='command')

class MessageModel(BaseDatabaseModel):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    information = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, server_default=func.now())

    command_id = Column(Integer, ForeignKey('commands.id'))
    command = relationship('CommandModel', back_populates='messages')

class DepartmentModel(BaseDatabaseModel):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    command_id = Column(Integer, ForeignKey('commands.id'))
    command = relationship('CommandModel', back_populates='departments')

    users = relationship('UserModel', back_populates='department')