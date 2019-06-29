import sys
from dataclasses import dataclass
from collections import defaultdict, deque

@dataclass
class Room:
    north: bool = False
    west: bool = False
    south: bool = False
    east: bool = False

  
def build_rooms(rooms, inq: deque, ix, iy):
    x, y = ix, iy
    in_paren = False
    while inq:
        if not in_paren and (inq[0] == '|' or inq[0] == ')'):
            return
        d = inq.popleft()
        
        if d == 'N':
            rooms[(x, y)].north = True
            y -= 1
            rooms[(x, y)].south = True
        elif d == 'S':
            rooms[(x, y)].south = True
            y += 1
            rooms[(x, y)].north = True
        elif d == 'W':
            rooms[(x, y)].west = True
            x -= 1
            rooms[(x, y)].east = True
        elif d == 'E':
            rooms[(x, y)].east = True
            x += 1
            rooms[(x, y)].west = True
        elif d == '(':
            in_paren = True
            build_rooms(rooms, inq, x, y)
        elif d == '|':
            build_rooms(rooms, inq, x, y)
        elif d == ')':
            in_paren = False

def find_distances(rooms):
    ds = {}
    q = deque()
    q.append((0, 0, 0))

    while q:
        x, y, d = q.popleft()
        r = rooms[(x, y)]
        #print(x, y, d, r)
        if (x, y) not in ds:
            #print(x, y)
            ds[(x, y)] = d
            if r.west and (x-1, y) not in ds:
                q.append((x-1, y, d+1))
            if r.east and (x+1, y) not in ds:
                q.append((x+1, y, d+1))
            if r.north and (x, y-1) not in ds:
                q.append((x, y-1, d+1))
            if r.south and (x, y+1) not in ds:
                q.append((x, y+1, d+1))

    return ds


rooms = defaultdict(Room)
in_str = sys.stdin.read().strip()[1:-1]
build_rooms(rooms, deque(in_str), 0, 0)

ds = find_distances(rooms)
print(max(ds.values()))
print(sum(1 if l >= 1000 else 0 for l in ds.values()))
