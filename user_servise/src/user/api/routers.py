from fastapi import APIRouter, Query, status, HTTPException, Depends
from typing import Annotated, Optional
import logging

from src.authorization.dependences import get_user_organization_info
from src.authorization.domain.entity import UserOrganizationInfo

from src.user.api.schemas import UserCreateSchema, UserLoginSchema, UserUpdateSchema
from src.user.domain.servises import user_servise
from src.user.domain.exception import AlreadyExist, DontExist, AnotherMicroserviseError
from src.user.domain.entity import User

from src.authorization.domain.servises import TokenServiсe
from src.authorization.api.schemas import TokenPair

user_router = APIRouter(prefix='/user')

unexpected_error = 'Непредвиденная ошибка.'

@user_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=TokenPair)
async def user_create(user_create_data: UserCreateSchema, command_code: Annotated[Optional[str], Query()] = None) -> TokenPair:
    try:
        user = await user_servise.user_create(user_create_data, command_code)
    except AlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except AnotherMicroserviseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return TokenServiсe.get_tokens(user.id)

@user_router.post('/login', status_code=status.HTTP_200_OK, response_model=TokenPair)
async def user_create(user_login_data: UserLoginSchema) -> TokenPair:
    try:
        user = await user_servise.user_login(user_login_data)
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return TokenServiсe.get_tokens(user.id)

@user_router.put('/update', status_code=status.HTTP_204_NO_CONTENT)
async def user_update(user_update_data: UserUpdateSchema, 
                      user_organization_info: UserOrganizationInfo = Depends(get_user_organization_info)) -> None:
    try:
        await user_servise.user_update(user_organization_info, user_update_data)
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
@user_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(id: int, user_organization_info: UserOrganizationInfo = Depends(get_user_organization_info)) -> None:
    try:
        await user_servise.user_delete(user_organization_info, id)
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
@user_router.patch('/live', status_code=status.HTTP_204_NO_CONTENT)
async def user_undelete(id: int, user_organization_info: UserOrganizationInfo = Depends(get_user_organization_info)) -> None:
    try:
        await user_servise.user_undelete(user_organization_info, id)
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)

    
    