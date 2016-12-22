#!/usr/bin/env python3

import re
import itertools
from collections import deque

NODE_REGEX = re.compile(r"/dev/grid/\w+-x(\d+)-y(\d+)\s+" +
                        r"(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%")


class State:
    def __init__(self, grid, target_pos: (int, int)):
        self.grid = grid
        self.target_pos = target_pos
        self.hash = hash_state((grid, target_pos))


class Node:
    def __init__(self, cap, used):
        self.cap = cap
        self.used = used

    def __eq__(self, other):
        return self.empty() == other.empty() and self.wall() == other.wall()

    def __hash__(self):
        return hash((self.empty(), self.wall()))

    def __str__(self):
        return '#' if self.wall() else '_' if self.empty() else '.'

    def avail(self):
        return self.cap - self.used

    def wall(self):
        return self.used > 400

    def empty(self):
        return self.used == 0


def cleanup_grid(grid: list) -> list:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = Node(int(grid[i][j][2]), int(grid[i][j][3]))
    return grid


def hash_state(state: (list, (int, int))):
    return hash((tuple(map(tuple, state[0])), state[1]))


def make_new_grid_y(grid: list, i: int, j: int, new_i: int) -> list:
    orig_used = grid[i][j].used
    new_grid = list(grid)
    new_grid[new_i] = list(new_grid[new_i])
    new_grid[i] = list(new_grid[i])
    new_grid[i][j] = Node(new_grid[i][j].cap, 0)
    new_grid[new_i][j] = Node(new_grid[new_i][j].cap,
                              new_grid[new_i][j].used + orig_used)
    return new_grid


def make_new_grid_x(grid: list, i: int, j: int, new_j: int) -> list:
    orig_used = grid[i][j].used
    new_grid = list(grid)
    new_grid[i] = list(new_grid[i])
    new_grid[i][j] = Node(new_grid[i][j].cap, 0)
    new_grid[i][new_j] = Node(new_grid[i][new_j].cap,
                              new_grid[i][new_j].used + orig_used)
    return new_grid


def valid_moves(state: (list, (int, int))):
    grid, current_target_pos = state.grid, state.target_pos
    new_grids = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            move_target = current_target_pos == (i, j)
            if grid[i][j].empty() or grid[i][j].wall():
                continue

            if i > 0 and grid[i - 1][j].empty():
                new_grids.append(
                    State(make_new_grid_y(grid, i, j, i - 1),
                          (i - 1, j) if move_target else current_target_pos))
            if i < len(grid) - 1 and grid[i + 1][j].empty() and not move_target:
                new_grids.append(
                    State(make_new_grid_y(grid, i, j, i + 1),
                          (i + 1, j) if move_target else current_target_pos))
            if j > 0 and grid[i][j - 1].empty():
                new_grids.append(
                    State(make_new_grid_x(grid, i, j, j - 1),
                          (i, j - 1) if move_target else current_target_pos))
            if j < len(grid[i]) - 1 and grid[i][j + 1].empty() and not move_target:
                new_grids.append(
                    State(make_new_grid_x(grid, i, j, j + 1),
                          (i, j + 1) if move_target else current_target_pos))
    return new_grids


def heur_distance(state):
    empty_target_i, empty_target_j = max(0, state.target_pos[0] - 1), \
                                     max(0, state.target_pos[1] - 1)
    for i in range(len(state.grid)):
        for j in range(len(state.grid[i])):
            if state.grid[i][j].used == 0:
                empty_tgt_dist = abs(i - empty_target_i) \
                                 + abs(j - empty_target_j)
                return (state.target_pos[0] + state.target_pos[1]
                        + 2 * empty_tgt_dist)
    return state.target_pos[0] + state.target_pos[1] + 200


def print_state(s):
    for row in s.grid:
        for c in row:
            print(str(c), end="")
        print()
    input()


def main():
    with open("input.txt") as f:
        text = f.read()
    matches = [m.groups() for m in NODE_REGEX.finditer(text)]
    columns = []
    for _, g in itertools.groupby(matches, lambda m: m[0]):
        columns.append(list(g))

    grid = list(map(list, zip(*columns)))
    grid = cleanup_grid(grid)
    target_pos = (0, len(grid[0]) - 1)
    start_state = State(grid, target_pos)
    prev_states = set()
    start_to_state_distances = {start_state.hash: 0}
    start_to_f_distances = {start_state.hash: heur_distance(start_state)}
    states = deque([start_state])
    next_state_hashes = {start_state.hash}

    while states:
        s = states.popleft()
        if s.target_pos == (0, 0):
            print("Least moves:", start_to_state_distances[s.hash])
            return

        h = s.hash
        prev_states.add(h)
        next_state_hashes.remove(h)
        for new_s in valid_moves(s):
            new_h = new_s.hash
            if new_h in prev_states:
                continue

            start_new_dist = start_to_state_distances[h] + 1
            if new_h not in next_state_hashes:
                states.appendleft(new_s)
                next_state_hashes.add(new_h)
            elif start_new_dist >= start_to_state_distances[new_h]:
                # did not find new lower distance
                continue

            start_to_state_distances[new_h] = start_new_dist
            start_to_f_distances[new_h] = start_new_dist + heur_distance(new_s)

        states = deque(sorted(
            states, key=lambda st: start_to_f_distances[st.hash]))


main()
