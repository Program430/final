from src.user.database.models import UserModel
from src.user.domain.entity import User
from dataclasses import asdict

class UserMapper:
    @staticmethod
    def from_model_to_entity(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            status=user_model.status,
            command=user_model.command_id,
            department=user_model.department_id
        )
    @staticmethod
    def from_entity_to_model(user: User) -> UserModel:
        return UserModel(
            id = user.id,
            status = user.status,
            command_id = user.command,
            department_id = user.department
        )