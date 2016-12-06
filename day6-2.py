#!/usr/bin/env python3

import sys
from collections import Counter


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]
    columns = []

    with open(inputfile) as f:
        for line in f:
            for i in range(len(line.strip())):
                if len(columns) <= i:
                    columns.append(Counter([line[i]]))
                else:
                    columns[i].update([line[i]])

    print('Message', ''.join([c.most_common()[-1][0] for c in columns]))


main()
