from fastapi import Header, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.authorization.domain.servises import TokenServiсe
from src.authorization.domain.entity import UserOrganizationInfo
from src.authorization.outsideapi.repository import AuthorizationApi
from src.authorization.domain.exception import TokenError

security = HTTPBearer()

def get_user_id_from_token(authorization_token: str = Header(...)) -> int:
    if not authorization_token or not authorization_token.casefold().startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Пропущен заголовок авторизации."
        )
    
    token = authorization_token.split(" ")[1]

    try:
        return TokenServiсe.get_user_id_from_token(token)
    except TokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

async def get_user_organization_info(user_id: int = Depends(get_user_id_from_token)) -> UserOrganizationInfo:
    return await AuthorizationApi.get_user_organization_info(user_id)