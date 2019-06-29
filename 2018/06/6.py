import sys
from collections import defaultdict, Counter
from itertools import product

def ring(min_x, max_x, min_y, max_y):
    for i in range(min_x, max_x+1):
        for j in (min_y, max_y):
            yield i, j
    for i in (min_x, max_x):
        for j in range(min_y+1, max_y):
            yield i, j

grid = {}

points = list(enumerate(tuple(map(int, l.strip().split(', '))) for l in sys.stdin.readlines()))

min_x = min(map(lambda x: x[1][0], points))
max_x = max(map(lambda x: x[1][0], points))
min_y = min(map(lambda x: x[1][1], points))
max_y = max(map(lambda x: x[1][1], points))

for i, j in product(range(min_x, max_x+1), range(min_y, max_y+1)):
    min_found = 1e8
    min_name = None
    for name, (px, py) in points:
        d = abs(i-px) + abs(j-py)
        if d < min_found:
            min_found = d
            min_name = name
        elif d == min_found:
            min_name = None
    grid[(i, j)] = min_name

infinites = set()
for i, j in ring(min_x - 2, max_x + 2, min_y - 2, max_y + 2):
    min_found = 1e8
    min_name = None
    for name, (px, py) in points:
        d = abs(i-px) + abs(j-py)
        if d < min_found:
            min_found = d
            min_name = name
        elif d == min_found:
            min_name = None
    if min_name:
        infinites.add(min_name)

c = Counter()
c.update(filter(lambda x: x is not None and x not in infinites, grid.values()))
print(c.most_common()[0][1])

r = 1
cx, cy = min_x +(max_x-min_x)//2, min_y+(max_y-min_y)//2
res = 1
while True:
    f = False
    for i, j in ring(cx-r, cx+r, cy-r, cy+r):
        a = sum(abs(i-px)+abs(j-py) for _, (px, py) in points)
        #print(i, j, a)
        if a < 10000:
            res += 1
            f = True
    if f:
        r += 1
    else:
        break

print(res)