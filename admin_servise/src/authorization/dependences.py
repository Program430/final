from fastapi import Header, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from src.authorization.domain.servises import TokenServiсe
from src.user.domain.entity import User
from src.user.database.repository import UserSQLAlchemyRepository
from src.authorization.domain.exception import TokenError
from src.exception import *

from src.config import SECRET_KEY_BETWEEN_SERVISES

security = HTTPBearer()

def get_user_id_from_token(authorization_token: str = Header(...)) -> int:
    if not authorization_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    auth_type, _, token = authorization_token.partition(' ')

    if not auth_type.casefold() == "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization format. Expected: 'Bearer <token>'"
        )
    try:
        return TokenServiсe.get_user_id_from_token(token)
    except TokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

async def get_organization_info(user_id: int = Depends(get_user_id_from_token)) -> User:
    try:
        user = await UserSQLAlchemyRepository.get_by(id=user_id)

        if not user:
            raise DontExist('Пользователь с таким айди не зареган.')

    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logging.error('Ошибка в функции получения информации о клиенте ' + str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    return user

def secret_key_is_valid(secret_key: str = Header(...)) -> None:
    if secret_key != SECRET_KEY_BETWEEN_SERVISES:
        raise HTTPException(status_code=404)