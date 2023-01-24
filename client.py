import json
import socket


class CommandManager:
    username = None
    password = None
    last_command = None

    @classmethod
    def send(cls, command, s):
        if command.split()[0] != 'signup' and command.split()[0] != 'login':
            if cls.username and cls.password:
                split = command.split()
                split.insert(1, cls.username)
                split.insert(2, cls.password)
                command = ' '.join(split)
        s.sendall(bytes(command, 'utf-8'))
        cls.last_command = command

    @classmethod
    def receive(cls, s):
        server_response = json.loads(s.recv(1024).decode())
        if 'Logged in' in server_response:
            cls.username = cls.last_command.split()[1]
            cls.password = cls.last_command.split()[2]
        return server_response


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))

            while True:
                command = input('Send to the server: ').strip()
                if command:
                    CommandManager.send(command, s)

                    if command == 'stop':
                        break

                    server_response = CommandManager.receive(s)
                    print(f"{server_response}")
