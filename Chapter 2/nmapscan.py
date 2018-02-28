"""
TCP Port scanner using NMAP *Multi-Threaded*
Usage: python nmapscan.py <Target_Host>
"""
import nmap
import sys
import time
from threading import Thread

portlist = 'portlist.txt'
port_dict = {}


def nmapscan(tgthost, tgtport):
    """
    Takes Target host and port as parameters. Uses nmap for tcp scanning. Write port state to global dictionary
    :param tgthost: Target Host
    :param tgtport: Target Port
    :return: Writes port state to port_dict
    """
    nmscan = nmap.PortScanner()
    nmscan.scan(tgthost, tgtport)
    port_dict[int(tgtport)] = nmscan[tgthost]['tcp'][int(tgtport)]['state']


def main():
    if len(sys.argv) == 2:
        tgthost = sys.argv[1]
        threads = []
        print('\nScanning {}'.format(tgthost))
        start_time = time.time()
        with open(portlist, 'r') as pf:
            for line in pf.readlines():
                port = line.strip('\n')
                attempt = Thread(target=nmapscan, args=(tgthost, port))
                threads.append(attempt)
                attempt.start()
        for t in threads:
            t.join()
        end_time = time.time()
        print('Scan Report for: {}'.format(tgthost))
        for port in sorted(port_dict.keys()):
            print('tcp | {} |{}'.format(port, port_dict[port]))
        print('Scan Duration: {} seconds'.format(end_time - start_time))
    else:
        print('Usage: python nmapscan.py <Target_Host>')
        exit(1)


if __name__ == '__main__':
    main()
