import sys
from itertools import product
from array import array

WOOD, LUMBER, CLEAR = 0, 1, 2

grid = array('b')
h, w = 0, 0
for l in sys.stdin.readlines():
    l = l.strip()
    if l:
        w = len(l)
        h += 1
    for c in l:
        if c == '|':
            grid.append(WOOD)
        elif c == '.':
            grid.append(CLEAR)
        else:
            grid.append(LUMBER)

def coord(x, y):
    return y * w + x

def neighbors(x, y):
    if y > 0:
        yield (x, y-1)
        if x > 0:
            yield (x-1, y-1)
        if x < w - 1:
            yield (x+1, y-1)
    if x > 0:
        yield (x-1, y)
    if x < w - 1:
        yield (x+1, y)
    if y < h - 1:
        yield (x, y+1)
        if x > 0:
            yield (x-1, y+1)
        if x < w - 1:
            yield (x+1, y+1)

def atleast(iter, x):
    c = 0
    for v in iter:
        if v:
            c += 1
        if c >= x:
            return True
    return False

def run(rounds, grid):
    grid_a, grid_b = grid[:], grid[:]
    visited = {}
    r = 0
    while r < rounds:
        for i, j in product(range(w), range(h)):
            if grid_a[coord(i, j)] == CLEAR:
                if atleast((grid_a[coord(x, y)] == WOOD for (x, y) in neighbors(i, j)), 3):
                    grid_b[coord(i, j)] = WOOD
                else:
                    grid_b[coord(i, j)] = CLEAR
            elif grid_a[coord(i, j)] == WOOD:
                if atleast((grid_a[coord(x, y)] == LUMBER for (x, y) in neighbors(i, j)), 3):
                    grid_b[coord(i, j)] = LUMBER
                else:
                    grid_b[coord(i, j)] = WOOD
            else:
                if (atleast((grid_a[coord(x, y)] == LUMBER for (x, y) in neighbors(i, j)), 1) and
                    atleast((grid_a[coord(x, y)] == WOOD for (x, y) in neighbors(i, j)), 1)):
                    grid_b[coord(i, j)] = LUMBER
                else:
                    grid_b[coord(i, j)] = CLEAR

        grid_a, grid_b = grid_b, grid_a
        l = ''.join(map(str, grid_a))
        if l in visited:
            diff = r - visited[l]
            r += diff * ((rounds-1 - r) // diff)
            visited.clear()
        visited[l] = r
        r += 1

    wood_c = sum(1 if c == WOOD else 0 for c in grid_a)
    lumber_c = sum(1 if c == LUMBER else 0 for c in grid_a)

    return wood_c * lumber_c

print(run(10, grid))
print(run(1000000000, grid))