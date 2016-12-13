#!/usr/bin/env python3


INPUT = 1362
MAX_STEPS = 50


def parity(n: int) -> bool:
    parity = False
    while (n):
        parity = not parity
        n &= (n - 1)
    return parity


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
    pos = (1,1)
    states = [(pos, 0)]
    prev_states = []
    prev_step = 0
    result = None
    while states and states[0][1] <= MAX_STEPS:
        s = states.pop(0)
        prev_states.append(s)

        for m in moves(s):
            if (not previous_state(m, prev_states)
                    and not previous_state(m, states)):
                states.append(m)

    print("len(prev_states):", len(prev_states))


main()
