import os
import time
import socket
import logging

from constants import CHUNK_SIZE, CHUNK


def start_client(log_level="INFO", host="127.0.0.1", port=8080, count=None, own_host="127.0.0.1", own_port=9000):
    logger = logging.getLogger('client')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('client.log')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    server_address = (host, port)
    own_address = (own_host, own_port)

    size = len(CHUNK)

    logger.debug("Sending {} bytes from CHUNK".format(size))

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(own_address)

    i = 0
    while count is None or i < 1:
        logger.debug("Start loop {}".format(i))
        sock.sendto(str(size).encode(), server_address)
        signal, addr = sock.recvfrom(CHUNK_SIZE)

        if signal.decode() != "start":
            logger.debug("There was an error on the server")
            return exit(1)

        while True:
            sock.sendto(CHUNK, server_address)
            time.sleep(1)

        # Recv amount of data received by the server
        num_bytes, addr = sock.recvfrom(CHUNK_SIZE)

        logger.debug("Server received {} bytes".format(num_bytes.decode()))

    f.close()

    sock.close()


def main():
    start_client()


if __name__ == "__main__":
    main()
