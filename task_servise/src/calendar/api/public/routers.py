from fastapi import APIRouter, status, Depends, HTTPException, Body
from typing import Annotated, List

from src.common.token import get_user_id_from_token
from src.calendar.api.public.shemas import MeetingCreateSchema
from src.calendar.domain.entity import Meeting
from src.calendar.domain.servise import meeting_servise
from src.exception import BadRequest

meeting_router = APIRouter(prefix='/meeting')

error = 'Нередвиденная ошибка'

@meeting_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=Meeting)
async def create_meeting(meeting_potencial: MeetingCreateSchema, user_who_send_request_id: int = Depends(get_user_id_from_token)) -> Meeting:
    try:
        meeting = await meeting_servise.create_meeting(meeting_potencial, user_who_send_request_id)
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    return meeting
    
@meeting_router.post('/add_user_to_meeting', status_code=status.HTTP_204_NO_CONTENT)
async def add_user_to_meeting(task_id: int, user_who_send_request_id: int = Depends(get_user_id_from_token)):
    try:
        await meeting_servise.add_user_to_meeting(task_id, user_who_send_request_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    

@meeting_router.post('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete(task_id: int, user_who_send_request_id: int = Depends(get_user_id_from_token)):
    try:
        await meeting_servise.delete(task_id, user_who_send_request_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
@meeting_router.patch('/update', status_code=status.HTTP_204_NO_CONTENT)
async def update(task_id: int, user_who_send_request_id: int = Depends(get_user_id_from_token)):
    try:
        await meeting_servise.update(task_id, user_who_send_request_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
