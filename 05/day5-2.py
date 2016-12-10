#!/usr/bin/env python3

import sys, random
from hashlib import md5


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input word.")
        return

    inputword = sys.argv[1].encode()
    password = [None] * 8
    counter = 0
    foundChars = 0

    while foundChars < 8:
        hashed = md5(inputword + str(counter).encode()).hexdigest()
        if hashed[:5] == '00000':
            pos = int(hashed[5], 16)
            if pos < 8 and not password[pos]:
                foundChars += 1
                password[pos] = hashed[6]
        counter += 1

    print('Password', ''.join(password))


main()
