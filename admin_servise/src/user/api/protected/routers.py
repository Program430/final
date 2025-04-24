from fastapi import APIRouter, Query, Body, status, HTTPException, Depends
from typing import Annotated, Optional, List
import logging

from src.authorization.dependences import get_organization_info, secret_key_is_valid
from src.user.domain.entity import User

from src.user.domain.servises import user_servise
from src.exception import AlreadyExist, DontExist
from src.user.domain.entity import User

from src.authorization.domain.servises import TokenServise

user_protected_router = APIRouter(prefix='/protected/user')

unexpected_error = 'Непредвиденная ошибка.'

@user_protected_router.post('/add_user_to_command', status_code=status.HTTP_204_NO_CONTENT)
async def user_add_to_command(id: Annotated[int, Body()], code : Annotated[str, Body()], _ = Depends(secret_key_is_valid)) -> None:
    try:
        await user_servise.add_user_to_command(id, code)
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)


@user_protected_router.post('/delete_user_from_command', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_from_command(id: Annotated[int, Body()], _ = Depends(secret_key_is_valid)) -> None:
    try:
        await user_servise.delete_user_from_command(id)
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
@user_protected_router.get('/get_workers_from_my_department_id', status_code=status.HTTP_200_OK, response_model=List[int])
async def get_workers_from_my_department_id(id: Annotated[int, Body()] , _ = Depends(secret_key_is_valid)) -> List[int]:
    try:
        ids = await user_servise.get_workers_from_my_department_id(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return ids

