#!/usr/bin/env python3

import string
import sys

units:str = sys.stdin.read().strip()

def react(units):
    while True:
        i = 0
        any_found = False
        while i >= 0 and i < len(units) - 1:
            l_lower, r_lower = units[i].islower(), units[i+1].islower()
            if (l_lower != r_lower and units[i+1].lower() == units[i].lower()):
                units = units[:i] + units[i+2:]
                i -= 1
                any_found = True
            else:
                i += 1
        if not any_found:
            break
    return units

part1 = react(units)
print(len(part1))

min_length = 500000000

for c in string.ascii_lowercase:
    t = units[:]
    t = t.replace(c, '')
    t = t.replace(c.upper(), '')
    t = react(t)
    min_length = min(min_length, len(t))

print(min_length)