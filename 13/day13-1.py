#!/usr/bin/env python3


INPUT = 1362
DEST = (31, 39)


def parity(n: int) -> bool:
    par = False
    while n:
        par = not par
        n &= (n - 1)
    return par


def iswall(x, y) -> bool:
    if x < 0 or y < 0:
        return True
    coord_sum = x*x + 3*x + 2*x*y + y + y*y + INPUT
    return parity(coord_sum)


def moves(state) -> list:
    pos = state[0]
    d = state[1] + 1
    dirs = [
        ((pos[0] - 1, pos[1]), d),
        ((pos[0] + 1, pos[1]), d),
        ((pos[0], pos[1] - 1), d),
        ((pos[0], pos[1] + 1), d)
    ]
    return [s for s in dirs if not iswall(*s[0])]


def previous_state(s, prev_states):
    return any(s[0] == ps[0] for ps in prev_states)


def main():
    pos = (1, 1)
    states = [(pos, 0)]
    prev_states = []
    result = None
    while states:
        s = states.pop(0)
        prev_states.append(s)
        for m in moves(s):
            if m[0] == DEST:
                result = m
                states.clear()
                break
            elif not previous_state(m, prev_states):
                states.append(m)

    print("Results: pos:", result[0], "distance:", result[1])


main()
