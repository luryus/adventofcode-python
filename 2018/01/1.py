import itertools
import sys

in_values = [int(a) for a in sys.stdin]
print('Last state', sum(in_values))

state = 0
visited = set([state])
for v in itertools.cycle(in_values):
    state += v
    if state in visited:
        print('Twice:', state)
        break
    visited.add(state)

