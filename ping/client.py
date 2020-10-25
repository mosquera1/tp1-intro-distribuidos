import os
import pathlib
import socket
from constants import CHUNK_SIZE


def start_client(log_level="default", host="127.0.0.1", port=8080, count=None, own_host="127.0.0.1", own_port=9000):
    server_address = (host, port)
    own_address = (own_host, own_port)

    root_dir = os.path.abspath(os.getcwd())
    file = '/ping_file.txt'

    f = open(root_dir + file, "rb")
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0, os.SEEK_SET)

    print("Sending {} bytes from {}".format(size, file))

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(own_address)

    sock.sendto(str(size).encode(), server_address)
    signal, addr = sock.recvfrom(CHUNK_SIZE)

    if signal.decode() != "start":
        print("There was an error on the server")
        return exit(1)

    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        sock.sendto(chunk, server_address)

    # Recv amount of data received by the server
    num_bytes, addr = sock.recvfrom(CHUNK_SIZE)

    print("Server received {} bytes".format(num_bytes.decode()))

    f.close()
    sock.close()


def main():
    start_client()


if __name__ == "__main__":
    main()
