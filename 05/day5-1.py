#!/usr/bin/env python3

import sys
from hashlib import md5

def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input word.")
        return

    inputword = sys.argv[1].encode()
    password = ""
    counter = 0

    while len(password) < 8:
        hashed = md5(inputword + str(counter).encode()).hexdigest()
        if hashed[:5] == '00000':
            print('Found hash', counter, hashed)
            password += hashed[5]
        counter += 1

    print('Password', password)


main()
