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
        data_len = Utils.get_int_from_bytes(conn.recv(4))
        return conn.recv(data_len)

    def get_connection_command_tuple(self):
        if not self.sock:
            raise Exception("Server not running")
        self.sock: socket.socket
        conn, addr = self.sock.accept()
        data = self.get_conn_data(conn)
        return conn, Commands.decode_command(data)  # todo: this is wrong. In case of error while decoding,
        # can't send a response

    def send_result(self, conn: socket.socket, res: str):
        conn.sendall(Utils.get_encoded_string(res))
        conn.close()

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"Started server at port {self.port}.")
