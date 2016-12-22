#!/usr/bin/env python3

import re
from itertools import permutations


NODE_REGEX = re.compile(r"\/dev\/grid\/\w+-x(\d+)-y(\d+)\s+" +
                        r"(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%")


def main():
    with open("input.txt") as f:
        text = f.read()
    matches = [m.groups() for m in NODE_REGEX.finditer(text)]
    count = sum(1 for pair in permutations(matches, 2)
                if int(pair[0][3]) > 0 and int(pair[0][3]) <= int(pair[1][4]))
    print("Valid pairs", count)


main()
