#!/usr/bin/env python3

import itertools
import sys

ids: [str] = sys.stdin.readlines()

twos = sum(1 for i in ids if any(i.count(c) == 2 for c in i))
threes = sum(1 for i in ids if any(i.count(c) == 3 for c in i))

print(twos * threes)

for i, j in itertools.combinations(ids, 2):
    differ = 0
    idx = 0
    for k, (r, l) in enumerate(zip(i, j)):
        if r != l:
            differ += 1
            if differ > 1:
                break
            else:
                idx = k
    if differ == 1:
        res: str = i.rstrip()
        res = res[:idx] + res[idx+1:]
        print(res)
        break
