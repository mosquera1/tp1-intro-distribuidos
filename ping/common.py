import time
import socket
from constants import CHUNK, CHUNK_SIZE


def send_chunk(logger, server_address, sock, i):
    start_time = time.time()
    logger.debug("Start loop {} to address {}".format(i, server_address))
    try:
        sock.sendto(str(CHUNK_SIZE).encode(), server_address)
        signal, addr = sock.recvfrom(CHUNK_SIZE)

        if signal.decode() != "start":
            logger.error("There was an error on the server")
            return 0,0
    except socket.error:
        logger.error("couldn't connect to server")
        return 0,0

    sock.sendto(CHUNK, server_address)

    # Recv amount of data received by the server
    num_bytes, addr = sock.recvfrom(CHUNK_SIZE)
    elapsed_milliseconds = round((time.time() - start_time) * 1000, 1)

    try:
        bytes_received = int(num_bytes.decode())
    except ValueError:
        bytes_received = 0

    logger.info("{} bytes from {} udp_seq={} time {} ms".format(bytes_received, server_address[0], i + 1,
                                                                elapsed_milliseconds))

    return bytes_received, elapsed_milliseconds


def ping(count, statistics, server_address, sock, logger):
    start_time = time.time()

    count = 0 if count is None else int(count)

    logger.debug("count {}".format(count))
    statistics["lost"] = 0
    statistics["times"] = []
    statistics["server"] = server_address[0]

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
        statistics["count"] = i
        statistics["received"] = i - statistics["lost"]

        elapsed_milliseconds = round((time.time() - start_time) * 1000, 1)

        statistics["total_time"] = elapsed_milliseconds


def direct_server(sock, logger, data, addr):
    size = int(data.decode())
    logger.info("Incoming chunk with size {} from {}".format(size, addr))

    bytes_received = 0

    sock.sendto(b'start', addr)

    while bytes_received < size:
        logger.debug("server inner loop, bytes: {}, size: {}".format(bytes_received, size))
        data, addr = sock.recvfrom(CHUNK_SIZE)
        logger.info("Received chunk {} from".format(size, addr))
        bytes_received += len(data)

    logger.debug("bytes {}".format(str(bytes_received)))
    # Send number of bytes received
    sock.sendto(str(bytes_received).encode(), addr)

    logger.debug("Sent {}".format(str(bytes_received).encode()))
