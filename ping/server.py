import argparse
import socket
import logging

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

    logger.addHandler(fh)

    address = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(address)

    while True:
        logger.info("loop")
        data, addr = sock.recvfrom(CHUNK_SIZE)
        size = len(data.decode())
        logger.info("Incoming chunk with size {} from {}".format(size, addr))

        bytes_received = 0

        sock.sendto(b'start', addr)

        while bytes_received < size:
            logger.info("inner loop, bytes: {}, size: {}".format(bytes_received, size))
            data, addr = sock.recvfrom(CHUNK_SIZE)
            logger.info("Received chunk {} from".format(size, addr))
            bytes_received += len(data)

        logger.info("bytes {}".format(str(bytes_received)))
        # Send number of bytes received
        sock.sendto(str(bytes_received).encode(), addr)

        logger.info("Sent {}".format(str(bytes_received).encode()))


def main():
    args = parse_arguments()

    start_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
