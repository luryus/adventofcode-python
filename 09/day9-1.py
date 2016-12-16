#!/usr/bin/env python3

import re
import sys

MARKER_REGEX = re.compile(r"\((\d+)x(\d+)\)")


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile) as f:
        compressed = f.read().strip()
        decompressed = ""

        while True:
            m = MARKER_REGEX.search(compressed)
            if m:
                decompressed += compressed[:m.start()]
                compressed = compressed[m.end():]
                pattern_len = int(m.group(1))
                pattern_repeat = int(m.group(2))
                decomp_pattern = compressed[:pattern_len] * pattern_repeat

                decompressed += decomp_pattern
                compressed = compressed[pattern_len:]
            else:
                decompressed += compressed
                break

        print("Decompressed length:", len(decompressed))


main()
