#!/usr/bin/env python3

import sys
import re


def convert_char(char, secid):
    if char == '-':
        return ' '

    return chr((ord(char) - 97 + secid) % 26 + 97)


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]
    secid_pattern = re.compile(".*-(\d+)")

    with open(inputfile) as f:
        for line in f:
            secid = int(secid_pattern.match(line).group(1))
            decr = [convert_char(c, secid) for c in line if not c.isdigit()]
            name = ''.join(decr)

            if 'north' in name:
                print(name, secid)


main()
