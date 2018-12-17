#!/usr/bin/env python3

import sys


def move_up(digit: int) -> int:
    if digit > 3:
        digit -= 3
    return digit


def move_down(digit: int) -> int:
    if digit < 7:
        digit += 3
    return digit


def move_left(digit: int) -> int:
    if digit not in [1, 4, 7]:
        digit -= 1
    return digit


def move_right(digit: int) -> int:
    if digit not in [3, 6, 9]:
        digit += 1
    return digit


def get_code_digit(line: str) -> int:
    digit = 5
    for direction in line.strip():
        print('Moving to direction', direction)
        if direction == 'U':
            digit = move_up(digit)
        elif direction == 'D':
            digit = move_down(digit)
        elif direction == 'L':
            digit = move_left(digit)
        elif direction == 'R':
            digit = move_right(digit)
        else:
            raise RuntimeError('Invalid direction ' + direction)

    return digit


def main():
    if len(sys.argv) != 2:
        print("Invalid parameters. Give input file name.")
        return

    inputfile = sys.argv[1]

    code = []

    with open(inputfile, 'r') as f:
        for line in f:
            digit = get_code_digit(line)
            code.append(digit)

    print('Code:', ''.join(str(d) for d in code))


main()
