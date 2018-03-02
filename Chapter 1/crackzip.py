"""
Run a dictionary attack for cracking zip file passwords.

Usage: python crackzip.py <zip_filename> <dictionary_filename>
"""
import sys
import os
import zipfile
from threading import Thread


def extractfile(file, passwd):
    """
    Extract zipfile to a directory if password is correct.

    :param file: Zipfile object to be extracted
    :param passwd: Password
    :return:
    """
    try:
        zipf = zipfile.ZipFile(file)
        zipf.extractall(path=os.path.join(file[:-4]), pwd=str.encode(passwd))
        print('Password: {}'.format(passwd))
    except:
        pass


def main():
    if len(sys.argv) == 3:
        archive = sys.argv[1]
        pass_file = sys.argv[2]

        if not os.path.isfile(archive):
            print('Zipfile ({}) missing'.format(archive))
            exit(1)
        elif not os.access(archive, os.R_OK):
            print('{} Access Denied'.format(archive))
        elif not os.path.isfile(pass_file):
            print('Password file ({}) missing'.format(pass_file))
            exit(1)
        elif not os.access(pass_file, os.R_OK):
            print('{} Access Denied'.format(pass_file))
        else:
            with open(pass_file, 'r') as pf:
                for line in pf.readlines():
                    passwd = line.strip('\n')
                    attempt = Thread(target=extractfile, args=(archive,
                                                               passwd))
                    attempt.start()
    else:
        print('Usage: python crackzip.py <zip_filename> <dictionary_filename>')
        exit(1)


if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print('Time Taken: {} seconds'.format(time.time() - start_time))
