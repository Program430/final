from jose import jwt
from datetime import datetime, timedelta

from src.config import JWT_SECRET_KEY
from src.authorization.domain.exception import TokenError

class TokenServiсe:
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
       