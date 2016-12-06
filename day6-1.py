#!/usr/bin/env python3

import sys
from collections import Counter


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile) as f:
        cols = zip(*(line.strip() for line in f))
        counters = [Counter(col) for col in cols]

    print('Message', ''.join([c.most_common(1)[0][0] for c in counters]))


main()
