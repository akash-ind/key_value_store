from src.key_value_store.commands.command_dto import CommandDTO, CommandEnum
from src.exceptions.exceptions import InvalidCommandException


class Commands:

    @staticmethod
    def decode_command(command: bytes):
        command = command.decode("utf-8")
        command = command.split(" ")
        if len(command) == 2:
            command, options = command
        else:
            options = command[1:]
            command = command[0]
        command_enum = CommandEnum.get_command_enum(command)
        if command_enum == CommandEnum.GET:
            command_dto = CommandDTO(command_enum, options, None)
            command_dto.check_validity()
            return command_dto
        elif command_enum == CommandEnum.SET:
            command_dto = CommandDTO(command_enum, options[0], options[1])
            command_dto.check_validity()
            return command_dto
        else:
            raise InvalidCommandException(f"Command not found: {command}")

