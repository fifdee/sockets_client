import time
import json
import socket
import uuid


class CommandManager:
    username = None
    password = None
    login_command = None

    @classmethod
    def send(cls, command, s):
        if command.split()[0] == 'login':
            cls.login_command = command

        if command.split()[0] != 'signup' and command.split()[0] != 'login':
            if cls.username and cls.password:
                split = command.split()
                split.insert(1, cls.username)
                split.insert(2, cls.password)
                command = ' '.join(split)
        s.sendall(bytes(command, 'utf-8'))

    @classmethod
    def receive(cls, s):
        data = b''
        while True:
            part = s.recv(1024)
            data += part
            if len(part) < 1024:
                # either 0 or end of data
                break
        server_response = json.loads(data.decode())
        if 'Logged in' in server_response:
            cls.username = cls.login_command.split()[1]
            cls.password = cls.login_command.split()[2]
        return server_response


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.loop = True
        self.s = None

    @staticmethod
    def connect_(obj):
        obj.connect()

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.connect((self.host, self.port))

            while self.loop:
                self.update()

    def update(self):
        command = input('Send to the server: ').strip()
        if command:
            CommandManager.send(command, self.s)

            if command == 'stop':
                self.loop = False
                return

            server_response = CommandManager.receive(self.s)
            print(f"{server_response}")


class ClientLoopedDbQuery(Client):
    def update(self):
        CommandManager.send('uptime', self.s)
        print(CommandManager.receive(self.s))
        CommandManager.send('login fifdee 123123', self.s)
        print(CommandManager.receive(self.s))

        start = time.perf_counter()
        i = 1
        for _ in range(10):
            CommandManager.send('users', self.s)
            print(f'Response number {i}. Response: {CommandManager.receive(self.s)[:100]}')
            i += 1
        stop = time.perf_counter()
        print(f'Loop time: {round(stop - start, 2)} seconds.')

        self.loop = False
