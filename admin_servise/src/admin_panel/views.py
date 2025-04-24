from sqladmin import ModelView
from src.user.database.models import UserModel
from src.command.database.models import CommandModel
from src.command.database.models import DepartmentModel

class UserAdmin(ModelView, model=UserModel):
    form_include_pk = True

class CommandAdmin(ModelView, model=CommandModel):
    form_include_pk = True

class DepartmentAdmin(ModelView, model=DepartmentModel):
    form_include_pk = True