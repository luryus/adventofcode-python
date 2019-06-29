import sys
import re
import matplotlib.pyplot as plt 
import numpy as np
from collections import defaultdict
from itertools import product

with open('in.txt') as f:
    in_lines = f.readlines()
in_vals = [tuple(map(int, re.findall(r'-?\d+', l))) for l in in_lines if l.strip()]

r = 0

while True:
    min_x, min_y, max_x, max_y = 1e8, 1e8, -1e8, -1e8
    mtx = defaultdict(bool)
    r += 1
    for x0, y0, dx, dy in in_vals:
        x, y = x0 + r * dx , y0 + r*dy
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        mtx[(x, y)] = True

    if (max_x - min_x) > 400 or max_y - min_y > 400:
        continue
    
    bmap = np.zeros((max_y - min_y + 1, max_x - min_x + 1), dtype=float)
    for x, y in mtx:
        bmap[y - min_y, x - min_x] = 1
    print('bmap ready', r)
    plt.imshow(bmap)
    plt.show()

