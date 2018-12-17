#!/usr/bin/env python3

from itertools import combinations, permutations
from collections import deque


def shortest_distance(maze: [int], line_len: int, start: int, end: int):
    start_state = (start, 0)
    states = deque([start_state])
    visited = set()
    while states:
        s = states.popleft()
        if s[0] in visited:
            continue
        visited.add(s[0])
        if s[0] == end:
            return s[1]

        if s[0] > line_len and maze[s[0] - line_len] == 0:   # up
            states.append((s[0] - line_len, s[1] + 1))
        if s[0] < len(maze) - line_len and maze[s[0] + line_len] == 0:
            states.append((s[0] + line_len, s[1] + 1))
        if s[0] % line_len > 0 and maze[s[0] - 1] == 0:   # left
            states.append((s[0] - 1, s[1] + 1))
        if s[0] % line_len - 1 != 0 and maze[s[0] + 1] == 0:
            states.append((s[0] + 1, s[1] + 1))
    raise AssertionError("No path")


def main():
    with open("input.txt") as f:
        input_text = f.read()
    line_len = input_text.index('\n')
    input_text = input_text.replace('\n', '')
    start_pos = input_text.index('0')
    num_positions = [i for i in range(len(input_text))
                     if input_text[i].isdigit() and input_text[i] != '0']
    maze = [1 if c == '#' else 0 for c in input_text]

    target_pairs = combinations(num_positions + [start_pos], 2)
    distances = {a: shortest_distance(maze, line_len, *a)
                 for a in target_pairs}

    shortest1, shortest2 = float('inf'), float('inf')
    for perm in permutations(num_positions):
        perm = (start_pos,) + perm
        l = 0
        for i in range(0, len(perm) - 1):
            l += distances.get((perm[i], perm[i+1])) \
                 or distances.get((perm[i+1], perm[i]))
        l2 = l + (distances.get((perm[-1], start_pos))
                  or distances.get((start_pos, perm[-1])))
        if l < shortest1:
            shortest1 = l
        if l2 < shortest2:
            shortest2 = l2

    print("Part 1:", shortest1)
    print("Part 2:", shortest2)

main()
