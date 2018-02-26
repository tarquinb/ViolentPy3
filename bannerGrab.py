"""Try Grab Banner from ports 1 - 1000"""

import socket
from numpy import arange as arange


def get_banner(ip, port):

    socket.setdefaulttimeout(2)
    s = socket.socket()
    banner = {}
    for p in port:
        try:
            s.connect((ip, p))
            banner[p] = s.recv(1024)
            s.close()
        except:
            pass
    return banner


def main():
    port = list(arange(1, 10001))
    ip = '10.10.10.3'

    banner = get_banner(ip, port)

    for key in list(banner.keys()):
        print('IP: {} PORT: {} \n'.format(ip, key))
        print(banner[key])
    return 0


if __name__ == "__main__":

    main()