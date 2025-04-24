from src.user.database.models import UserModel
from src.user.domain.entity import User
from dataclasses import asdict

class UserMapper:
    def from_model_to_entity(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            login=user_model.login,
            name=user_model.name,
            mail=user_model.mail,
            password=user_model.password,
            deleted_time=user_model.deleted_time
        )
    
    def from_entity_to_model(user: User) -> UserModel:
        return UserModel(**asdict(user))