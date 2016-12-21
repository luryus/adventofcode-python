#!/usr/bin/env python3

import re
from collections import deque


SWAP_POS_REGEX = re.compile(r"swap position (\d+) with position (\d+)")
SWAP_LETTER_REGEX = re.compile(r"swap letter (\w) with letter (\w)")
ROTATE_REGEX = re.compile(r"rotate (left|right) (\d+) steps?")
ROTATE_POS_REGEX = re.compile(r"rotate based on position of letter (\w)")
REVERSE_REGEX = re.compile(r"reverse positions (\d+) through (\d+)")
MOVE_REGEX = re.compile(r"move position (\d+) to position (\d+)")


def swap_pos(text: list, args) -> list:
    x, y = int(args[0]), int(args[1])
    text[x], text[y] = text[y], text[x]
    return text


def swap_letter(text: list, args) -> list:
    a, b = args[0], args[1]
    return [b if c == a else (a if c == b else c) for c in text]


def rotate(text: list, args) -> list:
    factor = 1 if args[0] == 'right' else -1
    count = int(args[1]) * factor
    d = deque(text)
    d.rotate(count)
    return list(d)


def rotate_pos(text: list, args) -> list:
    letter_pos = text.index(args[0])
    count = 1 + letter_pos + (1 if letter_pos >= 4 else 0)
    d = deque(text)
    d.rotate(count)
    return list(d)


def reverse(text: list, args) -> list:
    x, y = int(args[0]), int(args[1])
    text[x:y+1] = text[y:None if x == 0 else x-1:-1]
    return text


def move(text: list, args) -> list:
    x, y = int(args[0]), int(args[1])
    letter = text[x]
    del text[x]
    text.insert(y, letter)
    return text


FUNCS = [
    (SWAP_POS_REGEX, swap_pos),
    (SWAP_LETTER_REGEX, swap_letter),
    (ROTATE_REGEX, rotate),
    (ROTATE_POS_REGEX, rotate_pos),
    (REVERSE_REGEX, reverse),
    (MOVE_REGEX, move)
]


def main(start_word: str):
    text = list(start_word)
    with open("input.txt") as f:
        for row in f:
            for fun in FUNCS:
                m = fun[0].match(row)
                if m:
                    text = fun[1](text, m.groups())
                    break
    print(''.join(text))


main("abcdefgh")
