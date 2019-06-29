#!/usr/bin/env python3

import itertools

import re
import sys

REGEX = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

ids: [str] = sys.stdin.readlines()

mtx = [None] * 1000 * 1000

clean_ids = set()

for l in ids:
    m = re.match(REGEX, l)
    if not m : break
    i = int(m.group(1))
    x = int(m.group(2))
    y = int(m.group(3))
    l = int(m.group(4))
    h = int(m.group(5))
    clean = True

    for yy in range(y, y+h):
        for xx in range(x, x+l):
            if mtx[yy*1000 + xx] is None:
                mtx[yy*1000 + xx] = (1, i)
            else:
                clean = False
                if mtx[yy*1000 + xx][1] in clean_ids and mtx[yy*1000 + xx][0] == 1:
                    clean_ids.remove(mtx[yy*1000 + xx][1])
                mtx[yy*1000 + xx] = (mtx[yy*1000 + xx][0] + 1, 0)
    if clean:
        clean_ids.add(i)

print(clean_ids)

print(sum(1 for i in mtx if i is not None and i[0] > 1))
