import argparse
import socket
import logging

from common import ping, direct_server

CHUNK_SIZE = 64


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def start_server(log_level=logging.INFO, host="127.0.0.1", port=8080):
    logger = logging.getLogger('server')
    logger.setLevel(log_level)

    fh = logging.FileHandler('server.log')
    fh.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    logger.addHandler(fh)
    logger.addHandler(ch)

    address = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)

    while True:
        logger.debug("server loop")
        data, addr = sock.recvfrom(CHUNK_SIZE)

        command = data.decode()

        if command == "r":
            data, addr = sock.recvfrom(CHUNK_SIZE)
            count = data.decode()
            print("addr", addr)

            ping(count, {}, addr, sock, logger)
            return
        elif command == "x":
            pass

        direct_server(sock, logger, data, addr)


def main():
    args = parse_arguments()

    start_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
