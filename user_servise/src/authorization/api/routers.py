from fastapi import APIRouter, Body, HTTPException, status
from typing import Annotated

from src.authorization.api.schemas import TokenPair
from src.authorization.domain.servises import TokenServiсe
from src.authorization.domain.exception import TokenError

token_router = APIRouter(prefix='/token')

@token_router.post('/refresh')
async def refresh_tokens(refresh_token: Annotated[str, Body()]) -> TokenPair:
    try:
        return TokenServiсe.get_new_tokens_from_refresh(refresh_token)
    except TokenError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

