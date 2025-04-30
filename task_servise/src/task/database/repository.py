from sqlalchemy import select, update
from typing import List, Optional

from src.logger import log_errors
from src.database import session_maker
from src.task.domain.repository import TaskDatabaseAbstractRepository
from src.task.database.mapper import TaskMapper
from src.mark.database.mapper import MarkMapper
from src.task.domain.entity import Task
from src.mark.domain.entity import Mark
from src.task.database.models import TaskModel
from src.mark.database.models import MarkModel

class TaskSqlAlchemyRepository(TaskDatabaseAbstractRepository):
    @log_errors
    @staticmethod
    async def create_tasks(tasks: List[Task]) -> List[Task]:
        task_models = [TaskMapper.to_model(task) for task in tasks]
        async with session_maker() as session:
            session.add_all(task_models)
    
            await session.commit()
            
            for task_model in task_models:
                await session.refresh(task_model)
                
            return [TaskMapper.to_entity(task_model) for task_model in task_models]
        
    @log_errors
    @staticmethod
    async def get_by(**kwargs) -> Optional[Task]:
        async with session_maker() as session:
            query = select(TaskModel).filter_by(**kwargs)
            results = await session.execute(query)

            result = results.scalars().first()

        if result is None:
            return None

        return TaskMapper.to_entity(result)
    
    @log_errors
    @staticmethod
    async def get_tasks_for_me(id: int) -> List[Task]:
        async with session_maker() as session:
            query = select(TaskModel).filter_by(user_who_take = id)
            results = await session.execute(query)

            tasks = results.scalars().all()

        return [TaskMapper.to_entity(task) for task in tasks]

    @log_errors
    @staticmethod
    async def get_tasks_i_send(id: int) -> List[Task]:
        async with session_maker() as session:
            query = select(TaskModel).filter_by(user_who_send = id)
            results = await session.execute(query)

            tasks = results.scalars().all()

        return [TaskMapper.to_entity(task) for task in tasks]
    
    @log_errors
    @staticmethod
    async def delete_tasks(task_ids: List[int]) -> None:
        async with session_maker() as session:
            tasks_to_delete = await session.execute(
                select(TaskModel).where(TaskModel.id.in_(task_ids))
            )
            tasks_to_delete = tasks_to_delete.scalars().all()
            
            for task in tasks_to_delete:
                await session.delete(task)
                
            await session.commit()

    @log_errors
    @staticmethod
    async def update(task: Task) -> None:
        async with session_maker() as session:
            query = (
                update(TaskModel)
                .where(TaskModel.id == task.id)
                .values(name = task.name, description = task.description, 
                        status = task.status, deadline=task.deadline)
            )
            
            await session.execute(query)
            await session.commit()

    @log_errors
    @staticmethod
    async def get_all_marks_by_who_take_id(id: int) -> List[Mark]:
        async with session_maker() as session:
            tasks_query = select(TaskModel).where(TaskModel.user_who_take == id)
            tasks_result = await session.execute(tasks_query)
            tasks = tasks_result.scalars().all()
            
            if not tasks:
                return []
            
            marks_query = (
                select(MarkModel)
                .where(MarkModel.task_id.in_([task.id for task in tasks]))
                .order_by(MarkModel.id)
            )
            
            marks_result = await session.execute(marks_query)
            marks = marks_result.scalars().all()
            
            return marks


