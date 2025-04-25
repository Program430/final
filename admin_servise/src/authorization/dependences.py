from fastapi import Header, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.authorization.domain.servises import TokenServise
from src.user.domain.entity import User
from src.user.database.repository import UserSQLAlchemyRepository
from src.authorization.domain.exception import TokenError
from src.exception import *

from src.config import SECRET_KEY_BETWEEN_SERVISES

security = HTTPBearer()

def get_user_id_from_token(authorization1: str = Header(...)) -> int:
    if not authorization1 or not authorization1.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Пропущен заголовок авторизации."
        )
    
    token = authorization1.split(" ")[1]

    try:
        return TokenServise.get_user_id_from_token(token)
    except TokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

async def get_organization_info(user_id: int = Depends(get_user_id_from_token)) -> User:
    try:
        user = await UserSQLAlchemyRepository.get_by(id=user_id)

        if not user:
            raise DontExist('Пользователь с таким айди не зареган.')

    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    return user

def secret_key_is_valid(secret_key: str = Header(...)) -> None:
    if secret_key != SECRET_KEY_BETWEEN_SERVISES:
        raise HTTPException(status_code=404)