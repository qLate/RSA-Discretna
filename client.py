import socket
import threading
from hashlib import sha256
from secrets import compare_digest
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
            hash=''
            all_msg=self.s.recv(1024).decode()
            if ' ' in all_msg:
                hash, msg = all_msg.split(' ', 1)
            else:
                msg=all_msg
            msg=int(msg)
            msg = pow(msg, self.private[1], self.private[0])
            final_msg=int_to_string(msg)
            sha256_digest=sha256(final_msg.encode('utf-8'))
            digest=sha256_digest.hexdigest()
            succesfulness='(got succesfully)' if compare_digest(hash, digest) or hash=='' else '(got unsuccesfully)'
            print(final_msg, succesfulness)

    def write_handler(self):
        while True:
            msg = input()
            sha256_digest=sha256(msg.encode('utf-8'))
            digest=sha256_digest.hexdigest()+' '
          
            str_int = string_to_int(msg)

            encoded = pow(str_int, self.server_public_key[1], self.server_public_key[0])
            self.s.send((digest+str(encoded)).encode())


if __name__ == "__main__":
    cl = Client("127.0.0.1", 9012, "b_g")
    cl.init_connection()

