from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from src.user.domain.entity import Status
from src.database import BaseDatabaseModel

class UserModel(BaseDatabaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    status = Column(Enum(Status), nullable=False, default=Status.WORKER)

    command_id = Column(Integer, ForeignKey('commands.id'))
    command = relationship('CommandModel', back_populates='users')

    department_id = Column(Integer, ForeignKey('departments.id', ondelete="SET NULL"))
    department = relationship('DepartmentModel', back_populates='users')
