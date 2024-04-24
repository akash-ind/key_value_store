from src.hash_table.hashtable import HashTable
from src.key_value_store.commands.command_dto import CommandDTO, CommandEnum
from src.exceptions.exceptions import InvalidCommandException


class DefaultExecutor:

    def __init__(self, hash_table: HashTable):
        self.hash_table = hash_table

    def execute_get(self, key):
        res = self.hash_table.get(key)
        if not res:
            return "Key not found"
        return res.__str__()

    def execute_put(self, key, value):
        is_success = self.hash_table.put(key, value)
        if is_success:
            return "Success"

    def execute_command(self, command: CommandDTO) -> str:
        if command.command == CommandEnum.GET:
            return self.execute_get(command.key)

        if command.command == CommandEnum.SET:
            return self.execute_put(command.key, command.value)

        raise InvalidCommandException("Command executor not found")
