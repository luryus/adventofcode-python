#!/usr/bin/env python3

import sys, re


INVALID_ABBA_REGEX = re.compile(r"\[[^\]\s]*?(\w)(?!\1)(\w)\2\1[^\]\s]*?\]")
ABBA_REGEX = re.compile(r"(\w)(?!\1)(\w)\2\1")


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile) as f:
        matches = (ABBA_REGEX.search(line) for line in f
                   if INVALID_ABBA_REGEX.search(line) is None)
        abbas = [m.group(0) for m in matches if m]
        print(abbas)
        print("Abba adresses", len(abbas))


main()
