import argparse
import socket
import logging
import json
from common import ping, direct_server

CHUNK_SIZE = 64


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-H", "--host", default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default="8080")

    return parser.parse_args()


def start_server(log_level=logging.DEBUG, host="127.0.0.1", port=8080):
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
        statistics = {}

        if command == "r":
            try:
                data, addr = sock.recvfrom(CHUNK_SIZE)
                count = data.decode()
                logger.debug("count: {}".format(count))

                ping(count, statistics, addr, sock, logger)
                logger.debug("statistics: {}".format(statistics))
                sock.sendto(json.dumps(statistics).encode(), addr)
            except socket.error:
                logger.error("error while sending reverse ping")
                pass
            continue
        elif command == "x":
            try:
                logger.debug("proxy")
                data, addr = sock.recvfrom(CHUNK_SIZE)
                destination_host = data.decode()
                data, addr = sock.recvfrom(CHUNK_SIZE)
                destination_port = int(data.decode())


                my_ping_address = (host, port+1)
                my_ping_address 
                non_blocking = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                non_blocking.bind(my_ping_address)
                non_blocking.setblocking(0)
                non_blocking.settimeout(3)

                if destination_port is None:
                    destination_port = 8080
                if destination_host is None:
                    destination_host = "127.0.0.1"

                destination_address = (destination_host, destination_port)

                logger.debug("destination_address: {}".format(destination_address))

                data, addr = sock.recvfrom(CHUNK_SIZE)
                count = data.decode()
                logger.debug("count: {}, destination_address: {}".format(count, destination_address))

                ping(count, statistics, destination_address, non_blocking, logger)
                logger.debug("statistics: {}".format(statistics))
                sock.sendto(json.dumps(statistics).encode(), addr)
            except socket.error:
                logger.error("error while sending proxy ping")
                pass

            continue

        try:
            direct_server(sock, logger, data, addr)
        except socket.error:
            logger.error("error while receiving direct ping")


def main():
    args = parse_arguments()

    start_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
