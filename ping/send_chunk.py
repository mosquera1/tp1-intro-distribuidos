import time
import socket
from constants import CHUNK, CHUNK_SIZE


def send_chunk(logger, server_address, sock, i):
    start_time = time.time()
    logger.debug("Start loop {}".format(i))
    try:
        sock.sendto(str(CHUNK).encode(), server_address)
        signal, addr = sock.recvfrom(CHUNK_SIZE)

        if signal.decode() != "start":
            logger.error("There was an error on the server")
            exit(1)
    except socket.error:
        logger.error("couldn't connect to server")
        exit(1)

    sock.sendto(CHUNK, server_address)

    # Recv amount of data received by the server
    num_bytes, addr = sock.recvfrom(CHUNK_SIZE)
    elapsed_milliseconds = round((time.time() - start_time) * 1000, 1)

    logger.info("{} bytes from {} udp_seq={} time {} ms".format(num_bytes.decode(), server_address[0], i + 1,
                                                                elapsed_milliseconds))

    try:
        bytes_received = int(num_bytes.decode())
    except ValueError:
        bytes_received = 0

    return bytes_received, elapsed_milliseconds
