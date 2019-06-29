import sys
from collections import deque

tracks = [list(l.strip('\n')) for l in sys.stdin.readlines()]
carts = deque()

for y, l in enumerate(tracks):
    for x, t in enumerate(l):
        if t in '<>v^':
            carts.append((t, x, y, 2))
            tracks[y][x] = '|' if t in '^v' else '-'

def turn_left(d):
    dirs = '>^<v'
    return dirs[(dirs.index(d) + 1) % 4]


def turn_right(d):
    dirs = '>^<v'
    return dirs[(dirs.index(d) - 1) % 4]

def tick():
    i = len(carts)
    while i > 0:
        i -= 1
        d, x, y, turn = carts.popleft()
        if d == '>':
            x += 1
        elif d == '<':
            x-=1
        elif d == '^':
            y -= 1
        elif d == 'v':
            y += 1
        curr_t = tracks[y][x]
        if curr_t == '/':
            if d in '^v':
                d = turn_right(d)
            else:
                d = turn_left(d)
        elif curr_t == '\\':
            if d in '^v':
                d = turn_left(d)
            else:
                d = turn_right(d)
        elif curr_t == '+':
            turn = (turn + 1) % 3
            if turn == 0:
                d = turn_left(d)
            elif turn == 2:
                d = turn_right(d)
        # check crash
        ci = next((a for a in carts if a[1] == x and a[2] == y), None)
        if ci:
            # Crashed
            print('Crash', x, y)
            carts.remove(ci)
            i -= 1
        else:
            carts.append((d, x, y, turn))
    return list(carts)

while True:
    tick()
    if len(carts) <= 1:
        print(carts)
        break
