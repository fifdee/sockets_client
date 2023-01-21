from client import Client

HOST = "127.0.0.1"
PORT = 65432

client = Client(HOST, PORT)
client.connect()
