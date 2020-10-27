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


def ping(count, statistics, server_address, sock, logger):
    start_time = time.time()

    logger.debug("count {}".format(count))
    statistics["lost"] = 0
    statistics["times"] = []

    i = 0

    while (count is None) or i < count:
        logger.debug("client loop, i: {}".format(i))
        (received, elapsed_milliseconds) = send_chunk(logger, server_address, sock, i)

        if received < CHUNK_SIZE:
            statistics["lost"] += 1
        else:
            statistics["times"].append(elapsed_milliseconds)

        time.sleep(1)
        i += 1

    sock.close()

    elapsed_milliseconds = round((time.time() - start_time) * 1000, 1)

    statistics["count"] = count
    statistics["server"] = server_address[0]
    statistics["received"] = count - statistics["lost"]
    statistics["total_time"] = elapsed_milliseconds


def direct_server(sock, logger, data, addr):
    size = len(data.decode())
    logger.info("Incoming chunk with size {} from {}".format(size, addr))

    bytes_received = 0

    sock.sendto(b'start', addr)

    while bytes_received < size:
        logger.debug("server inner loop, bytes: {}, size: {}".format(bytes_received, size))
        data, addr = sock.recvfrom(CHUNK_SIZE)
        logger.info("Received chunk {} from".format(size, addr))
        bytes_received += len(data)

    logger.info("bytes {}".format(str(bytes_received)))
    # Send number of bytes received
    sock.sendto(str(bytes_received).encode(), addr)

    logger.info("Sent {}".format(str(bytes_received).encode()))
