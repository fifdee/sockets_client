import json
import socket
import time


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            while True:
                command = input('Send to the server: ')
                s.sendall(bytes(command, 'utf-8'))

                if command == 'stop':
                    break

                server_response = json.loads(s.recv(1024).decode())
                print(f"{server_response}")
