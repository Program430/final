from fastapi import APIRouter, Query, Body, status, HTTPException, Depends
from typing import Annotated, Optional, List
import logging

from src.authorization.dependences import get_organization_info
from src.command.domain.entity import Command, Department, Message

from src.command.api.schemas import CommandCreateSchema
from src.command.domain.servises import command_servise
from src.exception import AlreadyExist, DontExist, PermissionException
from src.user.domain.entity import User

command_router = APIRouter(prefix='/command')
department_router = APIRouter(prefix='/department')

unexpected_error = 'Непредвиденная ошибка.'

@command_router.post('/create', status_code=status.HTTP_201_CREATED)
async def command_create(potencial_command_data: CommandCreateSchema, user_organization_info: User = Depends(get_organization_info)) -> Command:
    try:
        command = await command_servise.command_create(user_organization_info, potencial_command_data)
    except AlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return command

@department_router.post('/create', status_code=status.HTTP_201_CREATED) 
async def department_create(department_name: Annotated[str, Body()], user_organization_info: User = Depends(get_organization_info)) -> Department:
    try:
        department = await command_servise.department_create(user_organization_info, department_name)
    except AlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return department

@command_router.post('/create/message', status_code=status.HTTP_201_CREATED)
async def command_create(potencial_command_data: CommandCreateSchema, user_organization_info: User = Depends(get_organization_info)) -> Command:
    try:
        command = await command_servise.command_create(user_organization_info, potencial_command_data)
    except AlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return command

@command_router.get('/get/messages', status_code=status.HTTP_200_OK, response_model=List[Message])
async def command_create(user_organization_info: User = Depends(get_organization_info)) -> List[Message]:
    try:
        messages = await command_servise.messages_get(user_organization_info)
    except AlreadyExist as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=unexpected_error)
    
    return messages

    
    