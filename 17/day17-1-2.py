#!/usr/bin/env python3

from hashlib import md5
from collections import deque


INPUT = "qzthpkfp"
GRID_SIZE = 4


def doors_open(state: (int, int, str)) -> (bool, bool, bool, bool):
    hashed = md5((INPUT + state[2]).encode()).hexdigest()[:4]
    # up, down, left, right
    res = [False] * 4
    for i in range(4):
        res[i] = hashed[i] in "bcdef"
    return tuple(res)


def next_states(state: (int, int, str)) -> list((int, int, str)):
    doors = doors_open(state)
    new_states = []
    if state[1] > 0 and doors[0]:
        new_states.append((state[0], state[1] - 1, state[2] + "U"))
    if state[1] < GRID_SIZE - 1 and doors[1]:
        new_states.append((state[0], state[1] + 1, state[2] + "D"))
    if state[0] > 0 and doors[2]:
        new_states.append((state[0] - 1, state[1], state[2] + "L"))
    if state[0] < GRID_SIZE - 1 and doors[3]:
        new_states.append((state[0] + 1, state[1], state[2] + "R"))
    return new_states


def main():
    states = deque()
    init_state = (0, 0, "")
    states.append(init_state)
    shortest_path, longest_path = None, None

    while states:
        s = states.popleft()
        if s[0] == s[1] == GRID_SIZE - 1:
            if shortest_path is None:
                shortest_path = s[2]
            if longest_path is None or len(longest_path) < len(s[2]):
                longest_path = s[2]
        else:
            states.extend(next_states(s))

    if shortest_path is None and longest_path is None:
        print("Path not found")

    print("Shortest:", shortest_path)
    print("Longest (len={}): {}".format(len(longest_path), longest_path))


main()
