"""
Try Grab Banner from ports 1 - 10000
Usage: python bannerGrab.py <vulnerability_list_filename>
"""

import socket
from numpy import arange as arange
import os
import sys


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


def check_vuln(ip, port, vuln_list, bannerstr):
    """
    Check for known vulnerable services against a pre-defined list of banners

    :param ip: IP address being scanned; type: str
    :param port: Port being scanned
    :param bannerstr: Banner being checked; type: str
    :return: 0
    """
    with open(vuln_list, 'r') as f:
        for line in f.readlines():
            if line.strip('\n') in bannerstr:
                print('IP {} PORT {}  VULN {}'.format(ip, port, line.strip('\n')))
            else:
                continue

    return 0


def main():
    if len(sys.argv) == 2:
        vuln_list = sys.argv[1]
        if not os.path.isfile(vuln_list):
            print('Vulnerability list ({}) missing'.format(vuln_list))
            exit(1)
        elif not os.access(vuln_list, os.R_OK):
            print('Access to Vulnerability List File Denied')
            exit(1)
        else:
            print('Scanning IP range 10.10.10.(1 - 255)')
            portlist = list(arange(1, 10001))
            banner = {}

            for i in arange(1, 255):
                ip = '10.10.10.' + str(i)                   # Change to reflect appropriate IP range
                banner[ip] = get_banner(ip, portlist)

            for ip in list(banner.keys()):
                for port in banner[ip].keys():
                    check_vuln(ip, port, vuln_list, str(banner[ip][port]))
    else:
        print('Usage: python bannerGrab.py <vulnerability_list_filename>')
        exit(1)

    return 0


if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    print('Time Taken: {} seconds'.format(time.time() - start_time))