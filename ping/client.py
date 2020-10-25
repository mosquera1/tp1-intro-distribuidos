import time
import socket
import logging
import signal
import argparse

from send_chunk import send_chunk
from constants import CHUNK, CHUNK_SIZE

statistics = {}


def print_statistics():
    print("----statistics-----")
    print(statistics)


def signal_handler(_, __):
    print_statistics()
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


def start_client(log_level="INFO", host="127.0.0.1", port=8080, count=None, own_host="127.0.0.1", own_port=9000):
    logger = logging.getLogger('client')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('client.log')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    server_address = (host, port)
    own_address = (own_host, own_port)

    size = len(CHUNK)
    logger.info("PING {} with {} bytes of data".format(host, size))
    logger.info("Server address {}".format(host))
    logger.info("Host address {}".format(own_address))

    # Create socket and connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(own_address)
    sock.setblocking(0)
    sock.settimeout(0.5)

    i = 0
    logger.debug("count {}".format(count))
    while (count is None) or i < count:
        (received, elapsed_milliseconds) = send_chunk(logger, server_address, sock, i)

        if received < CHUNK_SIZE:
            statistics["lost"] += 1

        time.sleep(1)
        i += 1

    statistics["count"] = i
    statistics["server"] = host
    statistics["received"] = i
    sock.close()
    print_statistics()


app_version = "1.0.0"
app_name = "Ping application"

help_base_text = '''usage : tp_ping . py [ - h ] [ - v | -q ] [ - s ADDR ] [ - p | -r | -x ] [ - c COUNT ] [ - d ADDR ]

{}

optional arguments :
-h , -- help show this help message and exit
-v , -- verbose increase output verbosity
-q , -- quiet decrease output verbosity
-s , -- server server IP address
-c , -- count stop after < count > replies
-p , -- ping direct ping
-r , -- reverse reverse ping
-x , -- proxy proxy pin
-d , -- dest-ip destination IP address
-dp , -- dest-port destination port address'''

default_ping_help_text = help_base_text.format(
    "no command selected")
direct_ping_help_text = help_base_text.format(
    "ping command is used to measure the latency between a client and a server")
reverse_ping_help_text = help_base_text.format(
    "reverse ping command is used to measure the latency between a server and a client")
proxy_ping_help_text = help_base_text.format(
    "proxy ping command is used to measure the latency between two servers")


def parse_arguments():
    parser = argparse.ArgumentParser(app_name, add_help=False)

    parser.add_argument("-h", "--help", help="print this and exit", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-q", "--quiet", help="decrease output verbosity", action="store_true")
    parser.add_argument("-s", "--server", help="server IP address", default="127.0.0.1")
    parser.add_argument("-c", "--count", help="stop after < count > replies", default=None)
    parser.add_argument("-p", "--ping", help="direct ping", action="store_true")
    parser.add_argument("-r", "--reverse", help="reverse ping", action="store_true")
    parser.add_argument("-x", "--proxy", help="proxy pin", action="store_true")
    parser.add_argument("-d", "--dest-ip", help="destination IP address", default=None)
    parser.add_argument("-dp", "--dest-port", help="destination Port address", default=None)

    return parser.parse_args()


def main():
    args = parse_arguments()

    (print_help, verbose, quiet, server, count, ping, reverse, proxy, destination_ip, destination_port) = (
        args.help, args.verbose, args.quiet, args.server, int(args.count) if not (args.count is None) else None,
        args.ping, args.reverse, args.proxy,
        args.dest_ip, args.dest_port
    )

    selected_types = sum([1 if x is True else 0 for x in (ping, reverse, proxy)])

    has_error = (verbose and quiet) or (proxy and (destination_ip is None))

    if (ping is False) and (reverse is False) and (proxy is False) or (selected_types > 1):
        print(default_ping_help_text)
        exit(0)

    if print_help is True or has_error is True:
        if ping:
            print(direct_ping_help_text)
            exit(0)
        if reverse:
            print(reverse_ping_help_text)
            exit(0)
        if proxy:
            print(proxy_ping_help_text)
            exit(0)

    print(app_name, app_version)

    log_level = logging.INFO
    if verbose:
        log_level = logging.DEBUG
    elif quiet:
        log_level = logging.ERROR

    if ping:
        port = 9000
        while port < 9010:
            try:
                return start_client(log_level=log_level, host=server, count=count, own_host="127.0.0.1", own_port=port)
            except socket.error:
                port += 1

    # if reverse:
    #     return start_client(log_level=log_level, server=server, count=count, own_host="127.0.0.1", own_port=9000)


if __name__ == "__main__":
    main()
