from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import BaseDatabaseModel

class UserIdModel(BaseDatabaseModel):
    __tablename__ = 'user_ids'

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'))

    meeting = relationship('MeetingModel', back_populates='users')

class MeetingModel(BaseDatabaseModel):
    __tablename__ = 'meetings'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String, nullable=False)
    who_create = Column(Integer)

    users = relationship('UserIdModel', back_populates='meeting', cascade="all, delete-orphan")
