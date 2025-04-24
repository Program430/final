from sqlalchemy import Column, Integer, DateTime, Enum, String
from sqlalchemy.orm import relationship

from src.database import BaseDatabaseModel
from src.task.domain.entity import TaskStatus

class TaskModel(BaseDatabaseModel):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    status = Column(Enum(TaskStatus), name="task_status_enum", nullable=False)
    description = Column(String, nullable=False)
    user_who_send = Column(Integer, nullable=False)
    user_who_take = Column(Integer, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    time_start = Column(DateTime(timezone=True), nullable=False)

    comments = relationship('CommentModel', back_populates='task', cascade="all, delete-orphan")
    marks = relationship('MarkModel', back_populates='task', cascade="all, delete-orphan")
    
