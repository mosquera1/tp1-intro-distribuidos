import argparse
from direct_ping import direct_ping

direct_ping()

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
        args.help, args.verbose, args.quiet, args.server, args.count, args.ping, args.reverse, args.proxy,
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


if __name__ == "__main__":
    main()
