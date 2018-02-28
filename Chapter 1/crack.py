"""
A standard dictionary attack with the dictionary and password files passed as command-line arguments

Usage: python crack.py <Hash Algorithm: sha512 / des> <dictionary_filename> <password_filename>
"""
import crypt
import hashlib
import sys
import os


def test_pass(crypt_pass, dict_file, algo):
    """
    Takes the encrypted password, dictionary file and hashing algorithm as parameters
    DES:
    strips out the salt from the first two characters of the encrypted password hash and returns either after finding
    the password or exhausting the words in the dictionary.
    SHA512:
    ID (A value of 1 denotes MD5; 2 or 2a is Blowfish; 3 is NT Hash; 5 is SHA-256; and 6 is SHA-512.), salt and hash
    separated by $ This function currently only supports SHA512.

    :param crypt_pass: Encrypted password
    :param dict_file: File containing common passwords (plaintext)
    :param algo: SHA-512 or DES
    :return: Results printed to console
    """
    if algo == ('des' or 'DES'):
        salt = crypt_pass[0:2]
        with open(dict_file, 'r') as f:
            for word in f.readlines():
                word = word.strip('\n')
                crypt_word = crypt.crypt(word, salt)

                if crypt_word == crypt_pass:
                    print('Found Password: {}\n'.format(word))
                    return
        print('Password not found')
        return
    elif algo == ('sha512' or 'SHA512'):
        salt = str.encode(crypt_pass.split('$')[2])
        with open(dict_file, 'r') as f:
            for word in f.readlines():
                word = str.encode(word.strip('\n'))
                crypt_word = hashlib.sha512(salt+word)
                if crypt_word.hexdigest() == crypt_pass.split('$')[3]:
                    print('Found Password: {}\n'.format(word.decode()))
                    return
    else:
        print('Supported hashing algorithms: des / sha512')
        exit(1)


def main():
    if len(sys.argv) == 4:
        algo = sys.argv[1]
        dict_file = sys.argv[2]
        pass_file = sys.argv[3]

        if not os.path.isfile(dict_file):
            print('Dictionary ({}) missing'.format(dict_file))
            exit(1)
        elif not os.access(dict_file, os.R_OK):
            print('{} Access Denied'.format(dict_file))
        elif not os.path.isfile(pass_file):
            print('Password file ({}) missing'.format(pass_file))
            exit(1)
        elif not os.access(pass_file, os.R_OK):
            print('{} Access Denied'.format(pass_file))
        else:
            with open(pass_file, 'r') as pf:
                for line in pf.readlines():
                    if ':' in line:
                        user = line.split(':')[0]
                        crypt_pass = line.split(':')[1].strip('\n')
                        print("Cracking password for: {}".format(user))
                        test_pass(crypt_pass, dict_file, algo)
    else:
        print('Usage: python crack.py <Hashing Algorithm: des / sha512> <dictionary_filename> <password_filename>')
        exit(1)
    return


if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print('Time Taken: {} seconds'.format(time.time() - start_time))
