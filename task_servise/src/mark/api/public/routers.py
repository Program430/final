from fastapi import APIRouter, status, Depends, HTTPException, Body
from typing import Annotated, List

from src.common.token import get_user_id_from_token
from src.mark.api.public.shemas import MarkCreateSchema
from src.mark.domain.entity import Mark
from src.mark.domain.servise import mark_servise
from src.exception import BadRequest

mark_router = APIRouter(prefix='/mark')

error = 'Нередвиденная ошибка'

@mark_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=Mark)
async def create_mark(mark: MarkCreateSchema, user_who_send_request_id: int = Depends(get_user_id_from_token)) -> Mark:
    try:
        tasks = await mark_servise.create_mark(mark, user_who_send_request_id)
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    return tasks
    
@mark_router.delete('/get_my_marks', status_code=status.HTTP_200_OK, response_model=List[Mark])
async def get_my_marks(user_who_send_request_id: int = Depends(get_user_id_from_token))-> List[Mark]:
    try:
        marks = await mark_servise.get_my_marks(user_who_send_request_id)
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    return marks
    
@mark_router.get('/get_average_marks_result', status_code=status.HTTP_200_OK, response_model=float)
async def get_average_marks_result(user_who_send_request_id: int = Depends(get_user_id_from_token))-> float: 
    try:
        tasks = await mark_servise.get_average_marks_result(user_who_send_request_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return tasks
    