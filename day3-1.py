#!/usr/bin/env python3

import sys
import re


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    valid_count = 0
    p = re.compile('\s*(\d+)\s*(\d+)\s*(\d+)\s*')

    with open(inputfile) as f:
        for line in f:
            if not line or line.isspace():
                continue

            m = p.match(line)
            if m:
                sides = sorted([int(side) for side in m.groups()])
                if sum(sides[:2]) > sides[2]:
                    print("{} + {} = {} > {}".format(
                        sides[0], sides[1],
                        sum(sides[:2]), sides[2]))
                    valid_count += 1
                else:
                    print("Not triangle:", sides)
            else:
                print("Invalid line!")

    print("Possible triangles:", valid_count)

main()
