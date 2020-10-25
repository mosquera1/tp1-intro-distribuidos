import argparse
import socket
import time
import os

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
-d , -- dest destination IP address'''

default_ping_help_text = help_base_text.format(
    "no command selected")
direct_ping_help_text = help_base_text.format(
    "ping command is used to measure the latency between a client and a server")
reverse_ping_help_text = help_base_text.format(
    "reverse ping command is used to measure the latency between a server and a client")
proxy_ping_help_text = help_base_text.format(
    "proxy ping command is used to measure the latency between two servers")


def parse_arguments():
    parser = argparse.ArgumentParser("Ping application", add_help=False)

    parser.add_argument("-h", "--help", help="print this and exit", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-q", "--quiet", help="decrease output verbosity", action="store_true")
    parser.add_argument("-s", "--server", help="server IP address", default="127.0.0.1")
    parser.add_argument("-c", "--count", help="stop after < count > replies", default=None)
    parser.add_argument("-p", "--ping", help="direct ping", action="store_true")
    parser.add_argument("-r", "--reverse", help="reverse ping", action="store_true")
    parser.add_argument("-x", "--proxy", help="proxy pin", action="store_true")
    parser.add_argument("-d", "--dest", help="destination IP address", default="127.0.0.1")

    return parser.parse_args()


def main():
    args = parse_arguments()

    (print_help, verbose, quiet, server, count, ping, reverse, proxy, destination_ip) = (
        args.help, args.verbose, args.quiet, args.server, args.count, args.ping, args.reverse, args.proxy,
        args.dest
    )

    if print_help and (ping is False) and (reverse is False) and (proxy is False):
        print(default_ping_help_text)
        exit(0)

    if print_help is True:
        if ping:
            print(direct_ping_help_text)
            exit(0)
        if reverse:
            print(reverse_ping_help_text)
            exit(0)
        if proxy:
            print(proxy_ping_help_text)
            exit(0)


if __name__ == "__main__":
    main()
