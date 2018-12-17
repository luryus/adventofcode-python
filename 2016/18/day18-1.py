#!/usr/bin/env python3


ROW_COUNT = 40


def is_trap(pos: int, prev_row: [bool]) -> bool:
    left = prev_row[pos - 1] if pos > 0 else False
    right = prev_row[pos + 1] if pos < len(prev_row) - 1 else False
    return left ^ right


def main():
    rows = []
    with open("input.txt") as f:
        first_row_input = f.read().strip()
    rows.append([c == '^' for c in first_row_input])
    row_len = len(first_row_input)

    while len(rows) < ROW_COUNT:
        rows.append([is_trap(i, rows[-1]) for i in range(row_len)])

    print('Safe spots:', sum(row.count(False) for row in rows))


main()
