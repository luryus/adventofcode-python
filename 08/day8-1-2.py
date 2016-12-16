#!/usr/bin/env python3

import re
import sys
from collections import deque

SCREEN_WIDTH = 50
SCREEN_HEIGHT = 6

RECT_REGEX = re.compile(r"rect (\d+)x(\d+)")
ROTATE_ROW_REGEX = re.compile(r"rotate row y=(\d+) by (\d+)")
ROTATE_COL_REGEX = re.compile(r"rotate column x=(\d+) by (\d+)")


def enable_rect(screen: list, width: int, height: int):
    print("rect width", width, "height", height)
    for i in range(height):
        screen[i][:width] = [1 for _ in range(width)]


def rotate_col(screen: list, index: int, by: int) -> list:
    transposed = list(zip(*screen))
    col = deque(transposed[index])
    col.rotate(by)
    transposed[index] = list(col)
    return list(map(list, zip(*transposed)))


def rotate_row(screen: list, index: int, by: int):
    row = deque(screen[index])
    row.rotate(by)
    screen[index] = list(row)


def print_screen(screen: list):
    for line in screen:
        print(''.join(map(lambda a: '#' if a else ' ', line)))


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]
    screen = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    with open(inputfile) as f:
        for line in f:

            line = line.strip()
            m = RECT_REGEX.match(line)
            if m:
                enable_rect(screen, int(m.group(1)), int(m.group(2)))
                continue
            m = ROTATE_ROW_REGEX.match(line)
            if m:
                rotate_row(screen, int(m.group(1)), int(m.group(2)))
                continue
            m = ROTATE_COL_REGEX.match(line)
            if m:
                screen = rotate_col(screen, int(m.group(1)), int(m.group(2)))
                continue

            print("Unknown line", line)

    print(sum(map(sum, screen)), "pixels on")
    print_screen(screen)


main()
