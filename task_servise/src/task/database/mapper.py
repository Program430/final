from src.task.domain.entity import Task
from src.task.database.models import TaskModel

class TaskMapper:
    @staticmethod
    def to_model(task: Task) -> TaskModel:
        return TaskModel(
            id=task.id,
            name=task.name,
            status=task.status,
            description=task.description,
            user_who_send=task.user_who_send,
            user_who_take=task.user_who_take,
            deadline=task.deadline,
            time_start=task.time_start
        )

    @staticmethod
    def to_entity(task_model: TaskModel) -> Task:
        return Task(
            id=task_model.id,
            name=task_model.name,
            status=task_model.status,
            description=task_model.description,
            user_who_send=task_model.user_who_send,
            user_who_take=task_model.user_who_take,
            deadline=task_model.deadline,
            time_start=task_model.time_start
        )