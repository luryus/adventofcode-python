#!/usr/bin/env python3

from collections import defaultdict
import sys
from queue import PriorityQueue


def dur(c):
    return ord(c) - 4

in_lines = [l.split(' ') for l in sys.stdin.readlines()]
in_lines = [(l[7], l[1]) for l in in_lines]

# deps, children
nodes = defaultdict(lambda: (set(), set()))

for node, dep in in_lines:
    nodes[node][0].add(dep)
    nodes[dep][1].add(node)

q = PriorityQueue()
roots = set()
handled = set()
for n, (deps, children) in nodes.items():
    if len(deps) == 0:
        q.put(n)
        roots.add(n)

part1 = ""
while not q.empty():
    n = q.get()
    part1 += n
    handled.add(n)
    for c in nodes[n][1]:
        if all(d in handled for d in nodes[c][0]):
            q.put(c)

print(part1)



q = PriorityQueue()
for n in roots:
    q.put(n)
workers = [(None, None)] * 5
handled = set()
for n, (deps, children) in nodes.items():
    if len(deps) == 0:
        q.put(n)

rounds = -1
while not q.empty() or any(w[0] is not None for w in workers):
    frees = []
    for i, (wjob, wtime) in enumerate(workers):
        if wjob is None:
            frees.append(i)
            continue
        wtime -= 1
        if wtime > 0:
            workers[i] = wjob, wtime
        else:
            workers[i] = (None, None)
            frees.append(i)
            handled.add(wjob)
            for c in nodes[wjob][1]:
                if all(d in handled for d in nodes[c][0]):
                    q.put(c)
    while not q.empty() and frees:
        i = frees.pop()
        n = q.get()
        workers[i] = (n, dur(n))
    rounds += 1
                
print(rounds)
