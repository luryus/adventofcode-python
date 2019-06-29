#!/usr/bin/env python3

from collections import Counter, defaultdict
import itertools
import re

import re
import sys

in_lines: [str] = sys.stdin.readlines()
in_lines.sort()

active_g = None
sleep_times = {}
start_min = None
shifts = defaultdict(lambda: [])
part2_cs = defaultdict(lambda: Counter())

for l in in_lines:
    l = l.strip()
    ns = list(map(int, re.findall(r'\d+', l)))
    if l.endswith("shift"):
        active_g = ns[-1]
    elif l.endswith("asleep"):
        start_min = ns[4]
    elif l.endswith('up'):
        shifts[active_g].append((start_min, ns[4]))
        part2_cs[active_g].update(range(start_min, ns[4]))
        prev_sleep = sleep_times.get(active_g, 0)
        sleep_times[active_g] = prev_sleep + ns[4] - start_min

max_slept = max(sleep_times.items(), key=lambda x: x[1])[0]
c = Counter()
for s in shifts[max_slept]:
    c.update(range(*s))
most_common_min = c.most_common(1)[0][0]

print('1:', max_slept * most_common_min)

max_repeats = max(map(lambda x: (x[0], x[1].most_common(1)[0]), part2_cs.items()),
    key=lambda x: x[1])
print(max_repeats[0]*max_repeats[1][0])