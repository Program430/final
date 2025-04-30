from dataclasses import asdict

from src.command.database.models import CommandModel, DepartmentModel, MessageModel
from src.command.domain.entity import Command, Department, Message

class CommandMapper:
    @staticmethod
    def from_model_to_entity(command_model: CommandModel) -> Command:
        return Command(
            id=command_model.id,
            name=command_model.name,
            description=command_model.description,
            code=command_model.code
        )
    @staticmethod
    def from_entity_to_model(command: Command) -> CommandModel:
        return CommandModel(**asdict(command))
    

class DepartmentMapper:
    @staticmethod
    def from_model_to_entity(department_model: DepartmentModel) -> Department:
        return Department(
            id=department_model.id,
            name=department_model.name,
            command=department_model.command_id,
        )
    @staticmethod
    def from_entity_to_model(department: Department) -> DepartmentModel:
        return DepartmentModel(
            id = department.id,
            name=department.name,
            command_id = department.command
        )
    

class MessageMapper:
    @staticmethod
    def from_model_to_entity(message_model: MessageModel) -> Message:
        return Message(
            id=message_model.id,
            name=message_model.name,
            command=message_model.command_id,
            info = message_model.info,
            date = message_model.date
        )
    @staticmethod
    def from_entity_to_model(message: Message) -> MessageModel:
        return MessageModel(
            id = message.id,
            name=message.name,
            command_id = message.command,
            info = message.info,
            date = message.date
        )