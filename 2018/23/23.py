from dataclasses import dataclass
from itertools import permutations, combinations, product
from collections import defaultdict, namedtuple
import re
import sys

Coord = namedtuple('Coord', ['x', 'y', 'z'])

@dataclass
class Nanobot:
    x: int
    y: int
    z: int
    r: int

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def in_range(self, other):
        return self.dist(other) <= self.r

    def intersect(self, other):
        return self.dist(other) <= (self.r + other.r)

    def __hash__(self):
        res = self.x
        res = 17*res + self.y
        res = 17*res + self.z
        return 17*res + self.r

rex = re.compile(r'(-?\d+)')
bots = []
for l in sys.stdin:
    nums = list(map(int, rex.findall(l)))
    bots.append(Nanobot(*nums))


def part1():
    strongest = max(bots, key=lambda x: x.r)
    inr = sum(1 if strongest.in_range(b) else 0 for b in bots)
    print(inr)

def find_best_search_boxes(full_box, side, bots):
    #print(full_box, side)
    min_x = full_box.x - side
    max_x = full_box.x + side
    min_y = full_box.y - side
    max_y = full_box.y + side
    min_z = full_box.z - side
    max_z = full_box.z + side

    best_bot_count = 0
    best_search_boxes = set()
    for boxx, boxy, boxz in product(
        range(min_x, max_x+1, side),
        range(min_y, max_y+1, side),
        range(min_z, max_z+1, side)):

        # calculate distance of each bot to the origin of the box
        # the origin becomes the "center" of the search box this way
        search_box = Nanobot(boxx, boxy, boxz, side)
        #print('SEARCH', search_box)
        bot_count = 0
        for b in bots:
            if search_box.intersect(b):
                bot_count += 1
        if bot_count > best_bot_count:
            best_search_boxes.clear()
            best_bot_count = bot_count
            best_search_boxes.add(search_box)
        elif bot_count == best_bot_count:
            best_search_boxes.add(search_box)
    return best_search_boxes, best_bot_count

def part2():
    min_x, max_x = min(b.x for b in bots), max(b.x for b in bots)
    min_y, max_y = min(b.z for b in bots), max(b.z for b in bots)
    min_z, max_z = min(b.y for b in bots), max(b.y for b in bots)
    w, h, d = max_x - min_x, max_y - min_y, max_z - min_z

    min_dim = min(w, h, d)
    max_dim = max(w, h, d)
    search_box_side = min_dim // 2
    search_boxes = [Nanobot(min_x + w//2, min_y + h//2, min_z + d//2, max_dim)]

    while search_box_side > 1:
        best_boxes = set()
        best_box_count = 0
        for b in search_boxes:
            bs, count = find_best_search_boxes(b, search_box_side, bots)
            if best_box_count < count:
                best_boxes.clear()
                best_box_count = count
            if best_box_count == count:
                best_boxes.update(bs)
        search_boxes = best_boxes
        search_box_side = (search_box_side % 2) + (search_box_side // 2)

    best_coord = None
    best_coord_bots = 0
    for box in search_boxes:
        c = sum(1 if bt.in_range(box) else 0 for bt in bots)
        if c > best_coord_bots:
            best_coord_bots = c
            best_coord = box

    print(best_coord.dist(Coord(0, 0, 0)), best_coord_bots)

part1()
part2()