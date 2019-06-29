import sys
from itertools import product
from array import array

def power(x, y, serial):
    rack = x + 10
    return (rack * y + serial) * rack % 1000 // 100 - 5

def square_power(grid, x, y, s):
    p = 0
    for dy in range(s):
        p += sum(grid[300*(y+dy)+x:300*(y+dy)+x+s])
    return p

grid = array('i', [0]*300*300)
serial = int(sys.stdin.read())

for x, y in product(range(300), range(300)):
    grid[y*300 + x] = (power(x+1, y+1, serial))

max_power = 0
max_coord = 0, 0
for x, y in product(range(300-2), range(300-2)):
    p = square_power(grid, x, y, 3)
    if p > max_power:
        max_power = p
        max_coord = x, y

max_coord = max_coord[0] + 1, max_coord[1] + 1
print(max_coord, max_power)

max_power = 0
max_coord = 0, 0, 0
prev_s_max = 0
decreases = 0
for s in range(2, 301):
    s_max = 0
    for x, y in product(range(300-s+1), range(300-s+1)):
        p = square_power(grid, x, y, s)
        if p > s_max: s_max = p
        if p > max_power:
            max_power = p
            max_coord = x, y, s
    if prev_s_max > s_max:
        decreases += 1
        if decreases > 5:
            break
    else:
        decreases = 0
    prev_s_max = s_max

max_coord = max_coord[0] + 1, max_coord[1] + 1, max_coord[2]
print(max_coord, max_power)

