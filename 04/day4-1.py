#!/usr/bin/env python3

import sys
import re


def valid_room_numbers(f):
    p = re.compile("([-a-z]+)-(\d+)\[([a-z]+)\]")
    matches = (p.match(line) for line in f)
    match_tuples = (match.groups() for match in matches)
    room_data = ((filter(lambda a: a != '-',
                         sorted(sorted(set(match_tuple[0])),
                                key=lambda a: match_tuple[0].count(a),
                                reverse=True)),
                  match_tuple[1], match_tuple[2])
                 for match_tuple in match_tuples)
    return (int(room[1]) for room in room_data
            if list(room[0])[:5] == list(room[2]))


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile) as f:
        print('Valid room numbers', sum(valid_room_numbers(f)))


main()
