#!/usr/bin/env python3

import sys

DIR_NORTH = 0
DIR_EAST = 1
DIR_SOUTH = 2
DIR_WEST = 3


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    with open(inputfile, 'r') as f:
        inputtext = f.read()

    if not inputtext:
        print("Invalid input file")
        return

    commands = inputtext.strip().split(', ')

    x = 0
    y = 0
    direction = DIR_NORTH

    for c in commands:
        if c[0] == 'L':
            direction = (direction - 1) % 4
        else:
            direction = (direction + 1) % 4

        distance = int(c[1:])
        if direction == DIR_NORTH:
            y -= distance
            print("Moving", distance, "north")
        elif direction == DIR_WEST:
            x -= distance
            print("Moving", distance, "west")
        elif direction == DIR_SOUTH:
            y += distance
            print("Moving", distance, "south")
        elif direction == DIR_EAST:
            x += distance
            print("Moving", distance, "east")

    print("x: {0}, y: {1}, distance: {2}".format(x, y, abs(x) + abs(y)))


main()
