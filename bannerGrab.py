"""Try Grab Banner from ports 1 - 10000"""

import socket
from numpy import arange as arange
import os

VULN_LIST = 'vuln_banners.txt'


def get_banner(ip, portlist):
    """
    Scan for and return banners from anIP across a port range

    :param ip: IP address to scan
    :param portlist: List of ports to scan
    :return: Dictionary -- {PORT:BANNER}
    """
    socket.setdefaulttimeout(2)
    banner = {}
    for port in portlist:
        try:
            s = socket.socket()
            print('Grabbing banner from {}:{}\n'.format(str(ip), port))
            s.connect((ip, port))
            banner[port] = s.recv(1024)
            s.detach()
        except:
            continue
    return banner


def check_vuln(ip, port, bannerstr):
    """
    Check for known vulnerable services against a pre-defined list of banners

    :param ip: IP address being scanned; str
    :param port: Port being scanned
    :param bannerstr: Banner being checked
    :return: 0
    """
    with open(VULN_LIST, 'r') as vulns:
        for line in vulns.readlines():
            if line.strip('\n') in bannerstr:
                print('IP {} PORT {}  VULN {}'.format(ip, port, line.strip('\n')))
            else:
                continue

    return 0


def main():
    if not os.path.isfile(VULN_LIST):
        print('Vulnerability list missing')
    else:
        portlist = list(arange(1, 10001))
        banner = {}

        for i in arange(3, 4):
            ip = '10.10.10.' + str(i)                   # Change to reflect appropriate IP range
            banner[ip] = get_banner(ip, portlist)

        for ip in list(banner.keys()):
            for port in banner[ip].keys():
                check_vuln(ip, port, str(banner[ip][port]))

    return 0


if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print('Time Taken: {} seconds'.format(time.time() - start_time))