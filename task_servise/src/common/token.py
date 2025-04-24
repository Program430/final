from jose import jwt
from fastapi import HTTPException, status, Header
from datetime import datetime, timedelta

from src.config import JWT_SECRET_KEY

def get_user_id_from_token(authorization1: str = Header(...)) -> int:
    if not authorization1 or not authorization1.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Пропущен заголовок авторизации."
        )
    
    token = authorization1.split(" ")[1]

    try:
        return get_id_from_token(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

def get_id_from_token(access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token, 
                JWT_SECRET_KEY, 
                algorithms=['HS256']
            )

        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не корректен.')
        
        if payload['type'] != 'access':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Нужно передавать access токен.')

        current_timestamp = datetime.utcnow().timestamp()
        if payload['exp'] < current_timestamp:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек.')
        
        return payload['id']

def generate_access_tokens(id: int) -> str:
    access_payload = {
        "id": id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "type": "access"
    }
    access_token = jwt.encode(access_payload, key=JWT_SECRET_KEY)

    return access_token