import sys
from collections import defaultdict

in_parts = sys.stdin.read().strip().split(" ")
nplayers = int(in_parts[0])
last_marble = 100 *int(in_parts[6])

curr_idx = 0
ring = [0]
scores = defaultdict(int)
turn = 0


for i in range(1, last_marble + 1):
    if i % 10000 == 0:
        print(i)
    if i % 23 == 0:
        scores[turn] = scores[turn] + i
        rem_idx = (curr_idx - 7) % len(ring)
        print(i, '% 23 == 0, removing', ring[rem_idx], 'from pos', rem_idx)
        scores[turn] = scores[turn] + ring.pop(rem_idx)
        curr_idx = rem_idx
    else:
        next_idx = (curr_idx + 2) % len(ring)
        # place
        ring.insert(next_idx, i)
        curr_idx = next_idx
    turn = (turn + 1) % nplayers
    #print(ring)

print(max(scores.items(), key=lambda x: x[1]))
