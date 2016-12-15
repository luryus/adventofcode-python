#!/usr/bin/env python3
# "inspiration" (= plagiation) from reddit


from itertools import product, combinations
from collections import deque


class State:
    def __init__(self, pairs: list, lift_pos: int, distance: int):
        self.pairs = sorted(pairs)
        self.lift_pos = lift_pos
        self.distance = distance

    def __hash__(self):
        return hash((tuple(self.pairs), self.lift_pos))

    def __eq__(self, other):
        pairseq = all(self.pairs[i] == other.pairs[i]
                      for i in range(len(self.pairs)))
        return pairseq and self.lift_pos == other.lift_pos

    def is_valid_state(self):
        lonely_mcs_indices = [i for i in range(len(self.pairs))
                              if self.pairs[i][0] != self.pairs[i][1]]
        for i in lonely_mcs_indices:
            fl = self.pairs[i][1]
            if any(p[0] == fl for p in self.pairs):
                return False
        return True

    def complete(self):
        return all(g == mc == 3 for g, mc in self.pairs)

    def valid_moves(self):
        floor_mc_pair_indices = [i for i in range(len(self.pairs))
                                 if self.pairs[i][1] == self.lift_pos]
        floor_gen_pair_indices = [i for i in range(len(self.pairs))
                                  if self.pairs[i][0] == self.lift_pos]

        zero_locked = all(p[0] != 0 and p[1] != 0 for p in self.pairs)
        one_locked = zero_locked and all(p[0] != 1 and p[1] != 1
                                         for p in self.pairs)

        new_moves = set()
        for mc_i, g_i in product(floor_mc_pair_indices,
                                 floor_gen_pair_indices):
            if self.lift_pos < 3:
                new_pairs = list(self.pairs)
                new_pairs[g_i] = (new_pairs[g_i][0] + 1, new_pairs[g_i][1])
                new_pairs[mc_i] = (new_pairs[mc_i][0], new_pairs[mc_i][1] + 1)
                new_moves.add(
                    State(new_pairs, self.lift_pos + 1, self.distance + 1))
            if ((self.lift_pos > 0 and not zero_locked)
                    or (self.lift_pos > 1 and not one_locked)
                    or self.lift_pos > 2):
                new_pairs = list(self.pairs)
                new_pairs[g_i] = (new_pairs[g_i][0] - 1, new_pairs[g_i][1])
                new_pairs[mc_i] = (new_pairs[mc_i][0], new_pairs[mc_i][1] - 1)
                new_moves.add(
                    State(new_pairs, self.lift_pos - 1, self.distance + 1))
        for mc_i1, mc_i2 in combinations(floor_mc_pair_indices, 2):
            if self.lift_pos < 3:
                new_pairs = list(self.pairs)
                new_pairs[mc_i1] = (new_pairs[mc_i1][0],
                                    new_pairs[mc_i1][1] + 1)
                new_pairs[mc_i2] = (new_pairs[mc_i2][0],
                                    new_pairs[mc_i2][1] + 1)
                new_moves.add(
                    State(new_pairs, self.lift_pos + 1, self.distance + 1))
            if ((self.lift_pos > 0 and not zero_locked)
                    or (self.lift_pos > 1 and not one_locked)
                    or self.lift_pos > 2):
                new_pairs = list(self.pairs)
                new_pairs[mc_i1] = (new_pairs[mc_i1][0],
                                    new_pairs[mc_i1][1] - 1)
                new_pairs[mc_i2] = (new_pairs[mc_i2][0],
                                    new_pairs[mc_i2][1] - 1)
                new_moves.add(
                    State(new_pairs, self.lift_pos - 1, self.distance + 1))
        for g_i1, g_i2 in combinations(floor_gen_pair_indices, 2):
            if self.lift_pos < 3:
                new_pairs = list(self.pairs)
                new_pairs[g_i1] = (new_pairs[g_i1][0] + 1,
                                   new_pairs[g_i1][1])
                new_pairs[g_i2] = (new_pairs[g_i2][0] + 1,
                                   new_pairs[g_i2][1])
                new_moves.add(
                    State(new_pairs, self.lift_pos + 1, self.distance + 1))
            if ((self.lift_pos > 0 and not zero_locked)
                    or (self.lift_pos > 1 and not one_locked)
                    or self.lift_pos > 2):
                new_pairs = list(self.pairs)
                new_pairs[g_i1] = (new_pairs[g_i1][0] - 1,
                                   new_pairs[g_i1][1])
                new_pairs[g_i2] = (new_pairs[g_i2][0] - 1,
                                   new_pairs[g_i2][1])
                new_moves.add(
                    State(new_pairs, self.lift_pos - 1, self.distance + 1))
        for mc_i in floor_mc_pair_indices:
            if self.lift_pos < 3:
                new_pairs = list(self.pairs)
                new_pairs[mc_i] = (new_pairs[mc_i][0], new_pairs[mc_i][1] + 1)
                new_moves.add(
                    State(new_pairs, self.lift_pos + 1, self.distance + 1))
            if ((self.lift_pos > 0 and not zero_locked)
                    or (self.lift_pos > 1 and not one_locked)
                    or self.lift_pos > 2):
                new_pairs = list(self.pairs)
                new_pairs[mc_i] = (new_pairs[mc_i][0], new_pairs[mc_i][1] - 1)
                new_moves.add(
                    State(new_pairs, self.lift_pos - 1, self.distance + 1))
        for g_i in floor_gen_pair_indices:
            if self.lift_pos < 3:
                new_pairs = list(self.pairs)
                new_pairs[g_i] = (new_pairs[g_i][0] + 1, new_pairs[g_i][1])
                new_moves.add(
                    State(new_pairs, self.lift_pos + 1, self.distance + 1))
            if ((self.lift_pos > 0 and not zero_locked)
                    or (self.lift_pos > 1 and not one_locked)
                    or self.lift_pos > 2):
                new_pairs = list(self.pairs)
                new_pairs[g_i] = (new_pairs[g_i][0] - 1, new_pairs[g_i][1])
                new_moves.add(
                    State(new_pairs, self.lift_pos - 1, self.distance + 1))

        return (m for m in new_moves if m.is_valid_state())


def main(part2=False):
    initial_pairs = [(0, 0), (0, 0), (1, 2), (1, 1), (1, 1)]
    if part2:
        initial_pairs.extend([(0, 0), (0, 0)])
    past_state_hashes = set()
    initial_state = State(initial_pairs, 0, 0)
    states = deque([initial_state])

    counter = 0

    while states:
        s = states.popleft()
        counter += 1
        if s.complete():
            print("Least moves:", s.distance)
            return

        past_state_hashes.add(hash(s))
        valid_moves = (m for m in s.valid_moves()
                       if hash(m) not in past_state_hashes
                       and hash(m) not in list(map(hash, states)))
        states.extend(valid_moves)


print("Part 1:")
main()
print("Part 2:")
main(True)
