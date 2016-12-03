#!/usr/bin/env python3

import sys


KEYPAD = [[None, None, '1', None, None],
          [None, '2', '3', '4', None],
          ['5', '6', '7', '8', '9'],
          [None, 'A', 'B', 'C', None],
          [None, None, 'D', None, None]]


def move_up(x: int, y: int) -> (int, int):
    if y > 0 and KEYPAD[y - 1][x]:
        y -= 1
    return x, y


def move_down(x: int, y: int) -> (int, int):
    if y < 4 and KEYPAD[y + 1][x]:
        y += 1
    return x, y


def move_left(x: int, y: int) -> (int, int):
    if x > 0 and KEYPAD[y][x - 1]:
        x -= 1
    return x, y


def move_right(x: int, y: int) -> (int, int):
    if x < 4 and KEYPAD[y][x + 1]:
        x += 1
    return x, y


def get_code_digit_coords(line: str, prevx: int, prevy: int) -> (int, int):
    x = prevx
    y = prevy
    for direction in line.strip():
        print('Moving to direction', direction)
        if direction == 'U':
            x, y = move_up(x, y)
        elif direction == 'D':
            x, y = move_down(x, y)
        elif direction == 'L':
            x, y = move_left(x, y)
        elif direction == 'R':
            x, y = move_right(x, y)
        else:
            raise RuntimeError('Invalid direction ' + direction)

    return x, y


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    code = []

    x = 0
    y = 2

    with open(inputfile, 'r') as f:
        for line in f:
            (x, y) = get_code_digit_coords(line, x, y)
            code.append(KEYPAD[y][x])

    print('Code:', ''.join(code))


main()
