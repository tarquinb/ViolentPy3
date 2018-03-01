"""
Establish SSH connectiongiven a host and user credentials.

usage: python autossh.py <host> <username> <password>
"""
import pexpect
import os
import sys
import time


def send_cmd(child, cmd):
    """
    Send commands to an SSH session
    :param child: SSH session
    :param cmd: Command String
    :return: Prints output from SSH session to console
    """
    child.sendline(cmd)
    child.expect([pexpect.EOF, pexpect.TIMEOUT, '# ', '>>> ', '> ', '\$ '])
    print('SSH session output\n')
    print(child.before)


def connect(user, host, passwd):
    """
    Takes a username, host and password. Establishes an SSH connection
    :param user: Username
    :param host: Host
    :param passwd: Password
    :return: SSH Connection
    """
    ssh_newkey = 'Are you sure you want to continue connecting'
    connstr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connstr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print('Error Connecting')
        exit(1)
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print('Error Connecting')
            exit(1)
    child.sendline(passwd)
    child.expect([pexpect.EOF, pexpect.TIMEOUT, '# ', '>>> ', '> ', '\$ '])
    return child


def main():
    if len(sys.argv) == 4:
        host = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        start_time = time.time()
        child = connect(user, host, passwd)
        send_cmd(child, 'cat /etc/shadow')
    else:
        print('usage: python autossh.py <host> <username> <password>')
        exit(1)


if __name__ == '__main__':
    main()
