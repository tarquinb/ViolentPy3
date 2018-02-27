"""Try Grab Banner from ports 1 - 1000"""

import socket
from numpy import arange as arange


def get_banner(s, ip, portlist):
    banner = {}
    for port in portlist:
        try:
            print('Connecting to {}:{}\n'.format(str(ip), port))
            s.connect((ip, port))
            banner[port] = s.recv(1024)
            print('Received Banner\n')
            s.detach()
        except:
            pass
    return banner


def main():
    portlist = list(arange(1, 100))
    banner = {}

    socket.setdefaulttimeout(2)
    s = socket.socket()

    for i in arange(1, 5):
        ip = '10.10.10.' + str(i)
        banner[ip] = get_banner(s, ip, portlist)

    for ip in list(banner.keys()):
        for port in banner[ip].keys():
            print('IP: {} PORT: {} \n'.format(ip, port))
            print(banner[ip][port])
    return 0


if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print('Time Taken: {} seconds'.format(time.time() - start_time))