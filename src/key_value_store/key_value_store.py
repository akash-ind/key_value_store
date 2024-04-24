import threading
from src.key_value_store.initialiser.thread_initialiser import ThreadInitializer
from src.key_value_store.commands.commands import Commands
from src.exceptions.exceptions import InvalidCommandException
from src.key_value_store.executer.default_executor import DefaultExecutor
from src.key_value_store.connector.connector import Connector


class KeyValueStore:

    def __init__(self):
        self.initializer = ThreadInitializer()
        self.commands = Commands()
        self.executor = None
        self.connector = Connector()
        self.compaction_thread = None

    def get_connection_command(self):
        try:
            return self.connector.get_connection_command_tuple()
        except InvalidCommandException as e:
            print(e)

    def send_result(self, conn, result):
        self.connector.send_result(conn, result)

    def start_db(self):
        while True:
            try:
                conn, command = self.get_connection_command()
                if not self.executor:
                    raise Exception("Executor not initialised")  # todo: Convert the exception
                self.executor: DefaultExecutor

                res = self.executor.execute_command(command)
                self.send_result(conn, res)
            except Exception as e:
                print(e)

    def get_hashtable(self):
        if not self.initializer.is_initialised():
            self.initializer.initialise()
        return self.initializer.get_hash_table()

    def run_compaction(self):
        compaction = self.initializer.get_compaction()
        compaction.run_compaction()

    def run(self):
        self.initializer.initialise()
        self.compaction_thread = threading.Thread(target=self.run_compaction)
        self.compaction_thread.start()
        self.executor = DefaultExecutor(self.initializer.get_hash_table())
        self.connector.start_server()
        self.start_db()

    def close(self):
        self.initializer.get_compaction().set_stop_compaction()
        self.compaction_thread.join()


if __name__ == "__main__":
    kv = KeyValueStore()
    try:
        kv.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        kv.close()
        exit(0)
