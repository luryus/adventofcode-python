#!/usr/bin/env python3

import re

MAX_IP = 0xFFFFFFFF

LIMIT_REGEX = re.compile(r"(\d+)-(\d+)")


def main():
    limits = []
    with open("input.txt") as f:
        for row in (LIMIT_REGEX.match(r) for r in f):
            if row:
                limits.append((int(row.group(1)), int(row.group(2))))
    limits.sort()

    open_count = 0
    current_block_start, current_block_end = limits[0]
    for l in limits[1:]:
        if l[0] > current_block_end + 1:
            # count the difference
            open_count += l[0] - current_block_end - 1
            current_block_start, current_block_end = l
        elif l[1] > current_block_end:
            current_block_end = l[1]

    # all iterated
    if current_block_end + 1 <= MAX_IP:
        open_count += MAX_IP - current_block_end

    print("Open IP count:", open_count)

main()
