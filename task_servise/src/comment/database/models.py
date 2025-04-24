from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import BaseDatabaseModel

class CommentModel(BaseDatabaseModel):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete="CASCADE"), nullable=False)
    description = Column(String, nullable=False)
    created_time = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    task = relationship('TaskModel', back_populates='comments')
