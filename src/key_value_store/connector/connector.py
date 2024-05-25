import socket
from src.key_value_store.commands.commands import Commands
from src.common.utils import Utils


class Connector:

    def __init__(self):
        self.sock = None
        self.host = "127.0.0.1"
        self.port = 8444

    @staticmethod
    def get_conn_data(conn: socket.socket):
        data_len = Utils.get_int_from_bytes(conn.recv(4))  # todo: Buggy code in case of multiple connections
        return conn.recv(data_len)

    def get_connection(self):
        if not self.sock:
            raise Exception("Server not running")
        self.sock: socket.socket
        conn, _ = self.sock.accept()
        return conn

    def get_command_from_conn(self, conn: socket.socket):
        data = self.get_conn_data(conn)
        return Commands.decode_command(data)

    def send_result(self, conn: socket.socket, res: str):
        conn.sendall(Utils.get_encoded_string(res))

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"Started server at port {self.port}.")
