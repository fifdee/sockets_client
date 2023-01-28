import unittest
from unittest.mock import Mock, MagicMock

from client import CommandManager


class CommandManagerTest(unittest.TestCase):
    def setUp(self):
        self.socket = Mock()

    def test_saving_last_command(self):
        CommandManager.last_command = None
        CommandManager.send('login username1 password1', self.socket)
        self.assertEqual('login username1 password1', CommandManager.last_command)

    def test_receiving_response_login_ok(self):
        self.socket.recv = MagicMock(return_value=b'"Logged in as username1"')
        CommandManager.last_command = 'login username1 password1'
        CommandManager.receive(self.socket)
        self.assertEqual('username1', CommandManager.username)
        self.assertEqual('password1', CommandManager.password)

    def test_receiving_response_login_wrong(self):
        CommandManager.username = None
        CommandManager.password = None
        self.socket.recv = MagicMock(return_value=b'"Incorrect credentials."')
        CommandManager.last_command = 'login username1 password1'
        CommandManager.receive(self.socket)
        self.assertEqual(None, CommandManager.username)
        self.assertEqual(None, CommandManager.password)

    def test_adding_login_credentials_to_command(self):
        CommandManager.username = 'username1'
        CommandManager.password = 'password1'
        CommandManager.send('whisper another_user message', self.socket)
        self.assertEqual('whisper username1 password1 another_user message', CommandManager.last_command)
