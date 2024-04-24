from typing import Optional
from enum import Enum
from dataclasses import dataclass
from src.exceptions.exceptions import InvalidCommandException


class CommandEnum(Enum):
    SET = "SET"
    GET = "GET"

    @classmethod
    def get_command_enum(cls, command: str) -> "CommandEnum":
        if not (command or isinstance(command, str)):
            raise InvalidCommandException()

        if command.upper() == cls.GET.value:
            return cls.GET
        if command.upper() == cls.SET.value:
            return cls.SET

        raise InvalidCommandException()


@dataclass(frozen=True)
class CommandDTO:
    command: CommandEnum
    key: str
    value: Optional[str]

    def check_validity(self):
        if not self.command:
            raise InvalidCommandException()

        if self.command == CommandEnum.GET:
            return True
        if self.command == CommandEnum.SET:
            if not self.value:
                raise InvalidCommandException("Value not given for set command")
            return True
        raise InvalidCommandException(f"Invalid command: {self.command.value}")
