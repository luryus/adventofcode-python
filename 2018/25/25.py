from dataclasses import dataclass
from itertools import combinations
import sys

class Star:
    x: int
    y: int
    z: int
    w: int
    siblings: list

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.siblings = []
        self.constellation = None

    def distance(self, other):
        return (abs(self.x - other.x) +
                abs(self.y - other.y) +
                abs(self.z - other.z) +
                abs(self.w - other.w))

    def __hash__(self):
        a = 17 * self.x
        a = 17 * a + self.y
        a = 17 * a + self.z
        return 17 * a + self.w


stars = []
for l in sys.stdin:
    if not l.strip():
        continue
    nums = [int(n) for n in l.strip().split(',')]
    stars.append(Star(*nums))

for sa, sb in combinations(stars, 2):
    if sa.distance(sb) <= 3:
        sa.siblings.append(sb)
        sb.siblings.append(sa)

def mark_constellation(root_node, const_id):
    root_node.constellation = const_id
    for n in root_node.siblings:
        if n.constellation is None:
            mark_constellation(n, const_id)

next_constellation_id = 0
for s in stars:
    if s.constellation is None:
        mark_constellation(s, next_constellation_id)
        next_constellation_id += 1

print(next_constellation_id)