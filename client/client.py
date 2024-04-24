import socket


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @staticmethod
    def encode_data(data):
        encoded_res = data.encode('utf-8')
        res_len = len(encoded_res)
        encoded_res_len = res_len.to_bytes(4, byteorder='big')
        return encoded_res_len + encoded_res

    @staticmethod
    def receive_data(conn):
        data_len = int.from_bytes(conn.recv(4), byteorder='big')
        return conn.recv(data_len)

    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            while True:
                data = input("Enter command: ")

                sock.sendall(self.encode_data(data))
                print(f"Sent data: {data}")
                received_data = self.receive_data(sock)
                print(f"Received data: {received_data.decode('utf-8')}")


if __name__ == "__main__":
    client = Client(host="127.0.0.1", port=8444)
    client.main()

