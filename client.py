import json
import socket


class CommandManager:
    username = None
    password = None
    last_command = None

    @classmethod
    def send(cls, command, s):
        if command != 'signup' and command != 'login':
            if cls.username and cls.password:
                command += f' {cls.username} {cls.password}'
        s.sendall(bytes(command, 'utf-8'))
        cls.last_command = command

    @classmethod
    def receive(cls, s):
        server_response = json.loads(s.recv(1024).decode())
        if server_response == 'Logged in.':
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
                command = input('Send to the server: ')
                CommandManager.send(command, s)

                if command == 'stop':
                    break

                server_response = CommandManager.receive(s)
                print(f"{server_response}")
