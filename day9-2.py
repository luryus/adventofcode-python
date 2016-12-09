#!/usr/bin/env python3

import sys, re
from collections import deque


MARKER_REGEX = re.compile(r"\((\d+)x(\d+)\)")


def decompressed_len(compressed: str) -> int:
    m = MARKER_REGEX.search(compressed)
    if m:
        before_len = m.start()
        compressed = compressed[m.end():]
        pattern_len = int(m.group(1))
        pattern_repeat = int(m.group(2))
        decomp_pattern_len = decompressed_len(compressed[:pattern_len]) \
                             * pattern_repeat

        return before_len + decomp_pattern_len \
                          + decompressed_len(compressed[pattern_len:])
    else:
        return len(compressed)


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile) as f:
        compressed = f.read().strip()

        print("Decompressed length:", decompressed_len(compressed))


main()
