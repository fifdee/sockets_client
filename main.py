import threading
import time

from client import Client, ClientLoopedDbQuery
from concurrent.futures import ProcessPoolExecutor


if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 65432

    # TESTING MULTIPLE CLIENTS SENDING QUERIES - AUTOMATICALLY
    clients = [ClientLoopedDbQuery(HOST, PORT) for _ in range(10)]
    t1 = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        executor.map(Client.connect_, clients)
    t2 = time.perf_counter()
    print(f'Overall time: {round(t2 - t1, 2)} seconds.')

    # NORMAL INSTANCE OF CLIENT ALLOWING TO TYPE COMMANDS
    # client = Client(HOST, PORT)
    # client.connect()
