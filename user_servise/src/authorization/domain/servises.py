from jose import jwt
from datetime import datetime, timedelta

from src.authorization.api.schemas import TokenPair
from src.config import JWT_SECRET_KEY
from src.authorization.domain.exception import TokenError

class TokenServise:
    @staticmethod
    def get_user_id_from_token(access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token, 
                JWT_SECRET_KEY, 
                algorithms=['HS256']
            )

        except:
            raise TokenError('Токен не корректен.')
        
        if payload['type'] != 'access':
            raise TokenError('Нужно передавать access токен.')

        current_timestamp = datetime.utcnow().timestamp()
        if payload['exp'] < current_timestamp:
            raise TokenError('Токен истек.')
        
        return payload['id']

    @classmethod
    def get_new_tokens_from_refresh(cls, refresh_token: str)-> TokenPair:
        try:
            payload = jwt.decode(
                refresh_token, 
                JWT_SECRET_KEY, 
                algorithms=['HS256']
            )

        except:
            raise TokenError('Токен не корректен.')
        
        if payload['type'] != 'refresh':
            raise TokenError('Нужно передавать refresh токен.')

        current_timestamp = datetime.utcnow().timestamp()
        if payload['exp'] < current_timestamp:
            raise TokenError('Токен истек.')
        
        return cls.get_tokens(payload['id'])

    @staticmethod
    def get_tokens(id: int) -> TokenPair:
        access_payload = {
            "id": id,
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "type": "access"
        }
        access_token = jwt.encode(access_payload, key=JWT_SECRET_KEY)

        refresh_payload = {
            "id": id,
            "exp": datetime.utcnow() + timedelta(days=7),
            "type": "refresh"
        }
        refresh_token = jwt.encode(refresh_payload, key=JWT_SECRET_KEY)

        return TokenPair(access_token=access_token, refresh_token=refresh_token)