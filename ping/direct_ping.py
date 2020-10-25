import threading
import os
from client import start_client
from server import start_server


def direct_ping(log_level="INFO", client_host="127.0.0.1", client_port=9000, server_host="127.0.0.1", server_port=8080,
                count=None):
    try:
        os.remove('server.log')
        os.remove('client.log')
    except FileNotFoundError:
        pass
    finally:
        pass

    server_thread = threading.Thread(target=start_server, args=(log_level, server_host, server_port))
    server_thread.start()

    client_thread = threading.Thread(target=start_client,
                                     args=(log_level, server_host, server_port, count, client_host, client_port))
    client_thread.start()


if __name__ == "__main__":
    direct_ping()
