import socket
import threading

import rsa
from string_int_converter import string_to_int


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_public_keys = {}

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        public, private = rsa.generate_keys()
        self.private = private

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append(c)

            # send public key to the client 
            client_public_key = [int(item) for item in c.recv(1024).decode().split()]
            self.client_public_keys[c] = client_public_key

            c.send(" ".join([str(item) for item in public]).encode())

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            user_public_key = self.client_public_keys[client]

            print(type(msg), msg)
            msg = string_to_int(msg)
            print(msg)
            msg = rsa.encrypt(msg, user_public_key[0], user_public_key[1])

            client.send(str(msg).encode())

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)


if __name__ == "__main__":
    s = Server(9000)
    s.start()
