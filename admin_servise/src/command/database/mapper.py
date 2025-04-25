from dataclasses import asdict

from src.command.database.models import CommandModel, DepartmentModel, MessageModel
from src.command.domain.entity import Command, Department, Message

class CommandMapper:
    def from_model_to_entity(command_model: CommandModel) -> Command:
        return Command(
            id=command_model.id,
            name=command_model.name,
            description=command_model.description,
            code=command_model.code
        )
    
    def from_entity_to_model(command: Command) -> CommandModel:
        return CommandModel(**asdict(command))
    

class DepartmentMapper:
    def from_model_to_entity(department_model: DepartmentModel) -> Department:
        return Department(
            id=department_model.id,
            name=department_model.name,
            command=department_model.command_id,
        )
    
    def from_entity_to_model(department: Department) -> DepartmentModel:
        return DepartmentModel(
            id = department.id,
            name=department.name,
            command_id = department.command
        )
    

class MessageMapper:
    def from_model_to_entity(message_model: MessageModel) -> Message:
        return Department(
            id=message_model.id,
            name=message_model.name,
            command=message_model.command_id,
            info = message_model.info,
            date = message_model.date
        )
    
    def from_entity_to_model(message: Message) -> MessageModel:
        return DepartmentModel(
            id = message.id,
            name=message.name,
            command_id = message.command,
            info = message.info,
            date = message.date
        )