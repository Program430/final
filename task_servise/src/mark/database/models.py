from sqlalchemy import Column, Integer, DateTime, Enum, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import BaseDatabaseModel
from src.mark.domain.entity import Scope

class MarkModel(BaseDatabaseModel):
    __tablename__ = 'marks'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    quality_score = Column(Enum(Scope), name='scope_enum')
    comment = Column(String)

    task = relationship('TaskModel', back_populates='marks')
    
