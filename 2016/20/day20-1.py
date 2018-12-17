#!/usr/bin/env python3

import re

LIMIT_REGEX = re.compile(r"(\d+)-(\d+)")


def main():
    limits = []
    with open("input.txt") as f:
        for row in (LIMIT_REGEX.match(r) for r in f):
            if row:
                limits.append((int(row.group(1)), int(row.group(2))))
    limits.sort()

    lowest_block_start, lowest_block_end = limits[0]
    for l in limits[1:]:
        if l[0] > lowest_block_end + 1:
            print("Lowest open IP:", lowest_block_end + 1)
            return
        else:
            lowest_block_end = l[1]

    print("All limits iterated")
    if lowest_block_end + 1 <= 0xFFFFFFFF:
        print("Lowest open IP:", lowest_block_end + 1)

main()
