#!/usr/bin/env python3


ROW_COUNT = 400000


def is_trap(pos: int, prev_row: [bool]) -> bool:
    left = prev_row[pos - 1] if pos > 0 else False
    right = prev_row[pos + 1] if pos < len(prev_row) - 1 else False
    return left ^ right


def main():
    with open("input.txt") as f:
        first_row_input = f.read().strip()
    prev_row = [c == '^' for c in first_row_input]
    row_len = len(first_row_input)
    counter = 1
    safe_tiles = prev_row.count(False)

    while counter < ROW_COUNT:
        new_row = [is_trap(i, prev_row) for i in range(row_len)]
        safe_tiles += new_row.count(False)
        prev_row = new_row
        counter += 1

    print('Safe tiles:', safe_tiles)


main()
