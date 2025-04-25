from fastapi import APIRouter, Query, status, HTTPException, Depends
from typing import Annotated, Optional, List
import logging

from src.authorization.dependences import get_organization_info
from src.user.domain.entity import User

from src.user.api.schemas import UserAssignSchema, MyWorkersResponseSchema
from src.user.domain.servises import user_servise
from src.exception import AlreadyExist, DontExist
from src.user.domain.entity import User

user_router = APIRouter(prefix='/user')

unexpected_error = 'Непредвиденная ошибка.'

@user_router.put('/assign', status_code=status.HTTP_204_NO_CONTENT)
async def user_assign(user_assign_data: UserAssignSchema, user_organization_info: User = Depends(get_organization_info)) -> None:
    try:
        await user_servise.user_assign(user_assign_data, user_organization_info)
    except AlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)


@user_router.get('/get_my_workers', status_code=status.HTTP_200_OK, response_model=List[MyWorkersResponseSchema])
async def get_my_workers(user_organization_info: User = Depends(get_organization_info)) -> List[MyWorkersResponseSchema]:
    try:
        workers = await user_servise.get_my_workers(user_organization_info)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return [MyWorkersResponseSchema(id = i.id, status=i.status, department=i.department) for i in workers]
    
    