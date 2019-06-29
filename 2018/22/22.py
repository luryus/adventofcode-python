from array import array
from itertools import product
from functools import lru_cache
from heapq import heappop, heappush

depth = 3198
tx, ty = 12,757
# depth = 510
# tx, ty = 10, 10

@lru_cache(maxsize=10000)
def erosion(x, y):
    return (geo_index(x, y) + depth) % 20183

def geo_index(x, y):
    if (x, y) == (0, 0) or (x, y) == (tx, ty):
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion(x-1, y) * erosion(x, y-1)

@lru_cache(maxsize=10000)
def gtype(x, y):
    return erosion(x, y) % 3

def coord(x, y):
    return y*(tx+1) + x

grid = array('b', [0] * (tx+1)*(ty+1))

for i, j in product(range(tx+1), range(ty+1)):
    grid[coord(i, j)] = gtype(i, j)

print(sum(grid))

CLIMB, TORCH, NONE = 0, 1, 2
ROCK, WET, NARROW = 0, 1, 2

def coord2(x, y):
    return y*(1500) + x

erosion_grid = array('i', [0] * (1500)*(ty*2+1))
for i, j in product(range(1500), range(ty*2+1)):
    erosion_grid[coord2(i, j)] = erosion(i, j)
print('erosion done')

def erosion2(x, y):
    if x < 1500 and y <= ty*2:
        return erosion_grid[coord2(x, y)]
    return (geo_index2(x, y) + depth) % 20183

def geo_index2(x, y):
    if (x, y) == (0, 0) or (x, y) == (tx, ty):
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion2(x-1, y) * erosion2(x, y-1)

def gtype2(x, y):
    if x <= tx and y <= ty:
        return grid2[coord2(x, y)]
    return erosion2(x, y) % 3

grid2 = array('b', [0] * (1500)*(ty*2+1))
for i, j in product(range(1500), range(ty*2+1)):
    grid2[coord2(i, j)] = erosion2(i, j) % 3

def compatible(x, y, tool):
    t = gtype2(x, y)
    if t == ROCK:
        return tool == CLIMB or tool == TORCH
    elif t == WET:
        return tool == CLIMB or tool == NONE
    else:
        return tool == TORCH or tool == NONE

@lru_cache(maxsize=100)
def heur(x, y, t):
    h = abs(tx - x) + abs(ty - y)
    if t == TORCH:
        return h
    else:
        return h + 7

# A*
visited = set()
work_queue = [(heur(0, 0, TORCH), 0, (0, 0), TORCH)]
i = 0

while work_queue:
    i += 1
    c, d, (x, y), tool = heappop(work_queue)
    if i % 1000 == 0:
        print(i, c, d, x, y, tool)
    # if i >= 210000:
    #     break
    if (x, y, tool) in visited:
        continue
    visited.add((x, y, tool))
    if (x, y, tool) == (tx, ty, TORCH):
        print(d)
        break
    t = gtype2(x, y)

    # tool changes
    if tool == NONE:
        if t == WET and (x, y, CLIMB) not in visited:
            heappush(work_queue, (heur(x, y, CLIMB) + d + 7, d + 7, (x, y), CLIMB))
        elif t == NARROW and (x, y, TORCH) not in visited:
            heappush(work_queue, (heur(x, y, TORCH) + d + 7, d + 7, (x, y), TORCH))
    elif tool == TORCH:
        if t == NARROW and (x, y, NONE) not in visited:
            heappush(work_queue, (heur(x, y, NONE) + d + 7, d + 7, (x, y), NONE))
        elif t == ROCK and (x, y, CLIMB) not in visited:
            heappush(work_queue, (heur(x, y, CLIMB) + d + 7, d + 7, (x, y), CLIMB))
    else:
        if t == WET and (x, y, NONE) not in visited:
            heappush(work_queue, (heur(x, y, NONE) + d + 7, d + 7, (x, y), NONE))
        elif t == ROCK and (x, y, TORCH) not in visited:
            heappush(work_queue, (heur(x, y, TORCH) + d + 7, d + 7, (x, y), TORCH))

    # move
    if x > 0 and compatible(x-1, y, tool) and (x-1, y, tool) not in visited:
        heappush(work_queue, (heur(x-1, y, tool)+d+1, d+1, (x-1, y), tool))
    if y > 0 and compatible(x, y-1, tool) and (x, y-1, tool) not in visited:
        heappush(work_queue, (heur(x, y-1, tool)+d+1, d+1, (x, y-1), tool))
    if compatible(x+1, y, tool) and (x+1, y, tool) not in visited:
        heappush(work_queue, (heur(x+1, y, tool)+d+1, d+1, (x+1, y), tool))
    if compatible(x, y+1, tool) and (x, y+1, tool) not in visited:
        heappush(work_queue, (heur(x, y+1, tool)+d+1, d+1, (x, y+1), tool))
