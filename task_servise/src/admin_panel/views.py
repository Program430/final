from sqladmin import ModelView
from src.task.database.models import TaskModel
from src.comment.database.models import CommentModel
from src.mark.database.models import MarkModel
from src.calendar.database.models import MeetingModel

class TaskAdmin(ModelView, model=TaskModel):
    pass

class CommentAdmin(ModelView, model=CommentModel):
    pass

class MarkAdmin(ModelView, model=MarkModel):
    pass

class MeetingAdmin(ModelView, model=MeetingModel):
    pass