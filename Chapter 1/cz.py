import zipfile
import sys
import os


def main():
    archive = sys.argv[1]
    passwd = 'SECRET'
    print(os.getcwd())
    zipf = zipfile.ZipFile(archive)
    zipf.extractall(pwd=str.encode(passwd))
    return 0


if __name__ == '__main__':
    main()