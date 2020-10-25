import argparse
import socket
import time
import os
import logging

from constants import CHUNK_SIZE


def get_timestamp():
    return int(round(time.time() * 1000))


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def start_server(log_level="INFO", host="127.0.0.1", port=8080):
    logger = logging.getLogger('server')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('server.log')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    address = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)

    while True:
        data, addr = sock.recvfrom(CHUNK_SIZE)
        size = len(data.decode())
        logger.debug("Incoming chunk with size {} from {}".format(size, addr))

        bytes_received = 0

        sock.sendto(b'start', addr)

        while bytes_received < size:
            data, addr = sock.recvfrom(CHUNK_SIZE)
            bytes_received += len(data)


        # Send number of bytes received
        sock.sendto(str(bytes_received).encode(), addr)

        logger.debug("Sent {}".format(str(bytes_received).encode()))


    sock.close()


def main():
    args = parse_arguments()

    start_server(args.host, args.port)


if __name__ == "__main__":
    main()
