#!/usr/bin/env python3

import sys
import re   # just trying regexes, not really needed here


LINE_PATTERN = re.compile('\s*(\d+)\s*(\d+)\s*(\d+)\s*')


def chunks(l, n):
    chunk = []
    for item in l:
        chunk.append(item)
        if len(chunk) >= n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def parse_line(line: str) -> list:
    m = LINE_PATTERN.match(line)
    if m:
        return [int(side) for side in m.groups()]
    else:
        raise AttributeError('Invalid line')


def side_groups(f):
    without_emptys = (line for line in f if (line and not line.isspace()))
    for line_chunk in chunks(without_emptys, 3):
        parsed = [parse_line(line) for line in line_chunk]
        for side_group in zip(*parsed):
            yield side_group


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    valid_count = 0

    with open(inputfile) as f:
        for sides in side_groups(f):
            sides = sorted(sides)
            if sum(sides[:2]) > sides[2]:
                valid_count += 1

    print("Possible triangles:", valid_count)


main()
