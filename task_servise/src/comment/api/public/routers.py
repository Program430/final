from fastapi import APIRouter, status, Depends, HTTPException, Body
from typing import Annotated, List

from src.common.token import get_user_id_from_token
from src.comment.api.public.shemas import CommentCreateSchema
from src.comment.domain.entity import Comment
from src.comment.domain.servise import comment_servise
from src.exception import BadRequest

task_comment_router = APIRouter(prefix='/task/comment')

error = 'Нередвиденная ошибка'

@task_comment_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=Comment)
async def create_comment(comment_potencial: CommentCreateSchema, user_who_send_request_id: int = Depends(get_user_id_from_token)) -> Comment:
    try:
        comment = await comment_servise.create_comment(comment_potencial, user_who_send_request_id)
    except BadRequest as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    
    return comment
    
@task_comment_router.get('/get_task_comments', status_code=status.HTTP_200_OK, response_model=List[Comment])
async def get_task_comment(task_id: int, user_who_send_request_id: int = Depends(get_user_id_from_token))-> List[Comment]:
    try:
        comments = await comment_servise.get_comments_for_task(task_id, user_who_send_request_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return comments