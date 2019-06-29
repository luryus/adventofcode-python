import sys
import re
from array import array
from itertools import product
from heapq import heappush, heappop

in_lines = sys.stdin.readlines()
num_regex = re.compile(r'\d+')

clay_veins = []
min_x, min_y, max_x, max_y = int(1e8), int(1e8), 0, 0
for l in in_lines:
    vals = [int(v) for v in num_regex.findall(l)]
    if l[0] == 'x':
        clay_veins.append((range(vals[0], vals[0]+1), range(vals[1], vals[2]+1)))
        min_x = min(vals[0], min_x)
        max_x = max(vals[0], max_x)
        min_y = min(min_y, vals[1])
        max_y = max(max_y, vals[2])
    elif l[0] == 'y':
        clay_veins.append((range(vals[1], vals[2]+1), range(vals[0], vals[0]+1)))
        min_y = min(vals[0], min_y)
        max_y = max(vals[0], max_y)
        min_x = min(min_x, vals[1])
        max_x = max(max_x, vals[2])

max_x += 1
min_x -= 1
w = max_x - min_x + 1
grid = array('b', [0] * w * (max_y+1))

def coord(x, y):
    return y * w + (x - min_x)

def write_grid(counter):
    for y in range(0, max_y+1):
        print(y%10, end='  ')
        for x in range(min_x, max_x+1):
            c = '.'
            v = grid[coord(x, y)]
            if v == 1: c = '#'
            elif v == 2: c = '|'
            elif v == 3: c = '~'
            print(c, end='')
        print()
    print()

visited = {}
wq = []

def flow(x, y, fromx, fromy, try_spread=True):
    if (x, y) in visited:
        return
    if y > max_y:
        return False
    visited[(x, y)] = (fromx, fromy)
    grid[coord(x, y)] = 2
    if y == max_y:
        return
    below = grid[coord(x, y+1)]

    if below == 0:
        heappush(wq, (-y-1, x, y+1, x, y))
    elif below == 1 or below == 3:
        # check siblings
        left_stop, right_stop = False, False
        all_filled = True
        xl, xr = x, x
        while True:
            xl -= 1
            if xl < min_x:
                break
            v = grid[coord(xl, y)]
            bv = grid[coord(xl, y + 1)]
            if v == 1:
                left_stop = True
                break
            elif v == 0:
                if (xl, y) not in visited:
                    heappush(wq, (-y, xl, y, fromx, fromy))
                all_filled = False
                if bv == 0 or bv == 2:
                    break
            elif v == 2 and (bv == 0 or bv == 2):
                break
        while True:
            xr += 1
            if xr > max_x:
                break
            v = grid[coord(xr, y)]
            bv = grid[coord(xr, y + 1)]
            if v == 1:
                right_stop = True
                break
            elif v == 0:
                if (xr, y) not in visited:
                    heappush(wq, (-y, xr, y, fromx, fromy))
                all_filled = False
                if bv == 0 or bv == 2:
                    break
            elif v == 2 and (bv == 0 or bv == 2):
                break
        if left_stop and right_stop and all_filled:
            for xs in range(xl+1, xr):
                grid[coord(xs, y)] = 3
            if (fromx, fromy) in visited:
                heappush(wq, (-fromy, fromx, fromy, *visited[(fromx, fromy)]))
                del visited[(fromx, fromy)]

for x_range, y_range in clay_veins:
    for x, y in product(x_range, y_range):
        grid[coord(x, y)] = 1

wq.append((0, 500, 0, None, None))
while wq:
    _, x, y, fromx, fromy = heappop(wq)
    flow(x, y, fromx, fromy)
print(sum(1 if v == 2 or v == 3 else 0 for v in grid[coord(min_x, min_y):]))
print(sum(1 if v == 3 else 0 for v in grid[coord(min_x, min_y):]))
