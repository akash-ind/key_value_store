import socket
from src.key_value_store.commands.commands import Commands


class Connector:

    def __init__(self):
        self.sock = None
        self.host = "127.0.0.1"
        self.port = 8444

    def get_connection_command_tuple(self):
        if not self.sock:
            raise Exception("Server not running")
        self.sock: socket.socket
        conn, addr = self.sock.accept()
        data = conn.recv(1024)
        while True:
            tmp = conn.recv(1024)
            if not tmp:
                break
            data += tmp
        return conn, Commands.decode_command(data)  # todo: this is wrong. In case of error while decoding,
        # can't send a response

    def send_result(self, conn: socket.socket, res: str):
        conn.sendall(res.encode('utf-8'))
        conn.close()

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
