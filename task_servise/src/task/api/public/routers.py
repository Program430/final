from fastapi import APIRouter, status, Depends, HTTPException, Body
from typing import Annotated, List

from src.common.token import get_user_id_from_token
from src.task.api.public.shemas import TaskCreateSchema, TaskUpdateSchema
from src.task.domain.entity import Task
from src.task.domain.servise import task_servise
from src.exception import BadRequest

task_router = APIRouter(prefix='/task')

error = 'Нередвиденная ошибка'

@task_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=List[Task])
async def create_task(task: TaskCreateSchema, user_who_send_request_id: int = Depends(get_user_id_from_token)) -> List[Task]:
    try:
        tasks = await task_servise.create_task(task, user_who_send_request_id)
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    return tasks
    
@task_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: Annotated[int, Body()], user_who_send_request_id: int = Depends(get_user_id_from_token)):
    try:
        await task_servise.delete_task(task_id, user_who_send_request_id)
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
@task_router.get('/get_tasks_for_me', status_code=status.HTTP_200_OK, response_model=List[Task])
async def get_task_for_me(user_who_send_request_id: int = Depends(get_user_id_from_token))-> List[Task]:
    try:
        tasks = await task_servise.get_tasks_for_me(user_who_send_request_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return tasks
    
@task_router.get('/get_tasks_i_send', status_code=status.HTTP_200_OK, response_model=List[Task])
async def get_task_i_send(user_who_send_request_id: int = Depends(get_user_id_from_token))-> List[Task]:
    try:
        tasks = await task_servise.get_tasks_i_send(user_who_send_request_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    return tasks
    
@task_router.patch('/update_task', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_to_update: TaskUpdateSchema, user_who_send_request_id: int = Depends(get_user_id_from_token))-> None:
    try:
        await task_servise.update_task(task_to_update, user_who_send_request_id)
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))