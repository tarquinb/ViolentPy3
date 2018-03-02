"""
Run a TCP Port scan using Full TCP Connections.

Usage: python tcpscanfull.py <host>
"""
import socket as skt
import sys
import time
from threading import Thread

portlist = 'portlist.txt'
port_dict = {}


def connscan(tgthost, tgtport):
    """
    Attempt a full TCP connection to determine if port is OPEN or CLOSED.

    :param tgthost: Target Host
    :param tgtport: Port to scan
    :return: {PORT: [STATUS, BANNER]} - written to global dictionary port_dict
    """
    try:
        connsock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        connsock.connect((tgthost, tgtport))
        results = connsock.recv(100)
        port_dict[tgtport] = ['OPEN', results.decode().strip('\n')]
        connsock.close()
    except:
        port_dict[tgtport] = ['CLOSED', '']


def portscan(tgthost, tgtports):
    """
    Scan target host over the range of ports using connscan().

    :param tgthost: Target Host
    :param tgtports: File containing list of ports to scan
    :return:
    """
    try:
        tgtip = skt.gethostbyname(tgthost)
    except:
        print('Cannot resolve {} : Unknown host'.format(tgthost))
        return
    try:
        tgtname = skt.gethostbyaddr(tgtip)
        print('\nScanning: {}'.format(tgtname[0]))
    except:
        print('\nScanning: {}'.format(tgtip))
    skt.setdefaulttimeout(2)
    threads = []
    with open(tgtports, 'r') as pf:
        for line in pf.readlines():
            port = int(line.strip('\n'))
            attempt = Thread(target=connscan, args=(tgthost, port))
            threads.append(attempt)
            attempt.start()
    for t in threads:                          # Wait for all threads to finish
        t.join()


def main():
    if len(sys.argv) == 2:
        tgthost = sys.argv[1]
        start_time = time.time()
        portscan(tgthost, portlist)
        end_time = time.time()
        for port in sorted(port_dict.keys()):
            print('{} TCP {} {}'.format(port, port_dict[port][0],
                                        port_dict[port][1]))
        print('Scan Duration: {} seconds'.format(end_time - start_time))
    else:
        print('Usage: python tcpscanfull.py <host>')
        exit(1)


if __name__ == '__main__':
    main()
