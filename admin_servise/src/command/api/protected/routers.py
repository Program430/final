from fastapi import APIRouter, Query, status, HTTPException, Depends, Body
from typing import Annotated, Optional
import logging

from src.authorization.dependences import secret_key_is_valid
from src.command.domain.servises import command_servise
from src.exception import AlreadyExist, DontExist
from src.command.domain.entity import Command

command_protected_router = APIRouter(prefix='/protected/command')

unexpected_error = 'Непредвиденная ошибка.'
    
@command_protected_router.post('/get_command_by_code', status_code=status.HTTP_200_OK)
async def get_command_by_code(code: Annotated[str, Body()], _ = Depends(secret_key_is_valid)) -> int:
    try:
        command = await command_servise.get_command_by_code(code)
    except DontExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)

    return command.id
