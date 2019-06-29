import sys
from collections import defaultdict, namedtuple

in_parts = sys.stdin.read().strip().split(" ")
nplayers = int(in_parts[0])
last_marble = 100*int(in_parts[6])

class Marble:
    def __init__(self, val, prev, next):
        self.val = val
        self.next = next
        self.prev = prev

curr_marble = Marble(0, None, None)
curr_marble.next = curr_marble
curr_marble.prev = curr_marble

scores = defaultdict(int)
turn = 0

for i in range(1, last_marble + 1):
    if i % 10000 == 0:
        print(i)
    if i % 23 == 0:
        scores[turn] = scores[turn] + i
        rem = curr_marble.prev.prev.prev.prev.prev.prev.prev
        scores[turn] = scores[turn] + rem.val
        rem.prev.next = rem.next
        rem.next.prev = rem.prev
        curr_marble = rem.next
    else:
        prev = curr_marble.next
        new = Marble(i, prev, prev.next)
        prev.next = new
        new.next.prev = new
        #print("inserted", new.val, "between", new.prev.val, new.next.val)
        curr_marble = new
    turn = (turn + 1) % nplayers

    m = curr_marble
    #print(m.val, end=" ")
    while m.next != curr_marble:
        m = m.next
        #print(m.val, end=" ")
    #print()

print(max(scores.items(), key=lambda x: x[1]))
