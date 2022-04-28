import socket
import threading

import rsa

from string_int_converter import int_to_string, string_to_int

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        public, private = rsa.generate_keys()
        self.private = private

        # exchange public keys
        self.s.send(" ".join([str(item) for item in public]).encode())

        server_public_key = [int(item) for item in self.s.recv(1024).decode().split()]
        self.server_public_key = server_public_key

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            msg = int(self.s.recv(1024).decode())
            msg = pow(msg, self.private[1], self.private[0])

            print(int_to_string(msg))

    def write_handler(self):
        while True:
            msg = input()

            str_int = string_to_int(msg)

            encoded = pow(str_int, self.server_public_key[1], self.server_public_key[0])
            self.s.send(str(encoded).encode())


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9000, "b_g")
    cl.init_connection()
