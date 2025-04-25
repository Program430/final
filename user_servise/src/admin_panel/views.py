from sqladmin import ModelView
from src.user.database.models import UserModel

class UserAdmin(ModelView, model=UserModel):
    pass