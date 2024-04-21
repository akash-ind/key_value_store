from src.hash_table.hashtable import HashTable
from src.key_value_store.commands.command_dto import CommandDTO, CommandEnum
from src.exceptions.exceptions import InvalidCommandException


class DefaultExecutor:

    def __init__(self, hash_table: HashTable):
        self.hash_table = hash_table

    def execute_command(self, command: CommandDTO):
        if command.command == CommandEnum.GET.value:
            return self.hash_table.get(command.key)

        if command.command == CommandEnum.SET.value:
            return self.hash_table.put(command.key, command.value)

        return InvalidCommandException("Command executor not found")
