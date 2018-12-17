#!/usr/bin/env python3

import sys
from hashlib import md5


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input word.")
        return

    inputword = sys.argv[1].encode()
    password = [''] * 8
    counter = 0
    found_chars = 0

    while found_chars < 8:
        hashed = md5(inputword + str(counter).encode()).hexdigest()
        if hashed[:5] == '00000':
            pos = int(hashed[5], 16)
            if pos < 8 and not password[pos]:
                found_chars += 1
                password[pos] = hashed[6]
        counter += 1

    print('Password', ''.join(password))


main()
