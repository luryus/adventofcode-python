import sys
from collections import deque

with open('test.txt', 'r') as f:
    in_lines = [l.strip() for l in sys.stdin.readlines() if l.strip()]
rows, cols = len(in_lines), len(in_lines[0])

def ranged(ux, uy, grid):
    r = []
    # up
    if grid[coord(ux, uy - 1)] is None:
        r.append((ux, uy-1))
    # left
    if grid[coord(ux -1, uy)] is None:
        r.append((ux -1, uy))
    # right
    if grid[coord(ux + 1, uy)] is None:
        r.append((ux + 1, uy))
    # down
    if grid[coord(ux, uy + 1)] is None:
        r.append((ux, uy +1))
    return r

def coord(x, y):
    return y * cols + x

def next_unit(us):
    return min(us, key=lambda u: coord(u.x, u.y))

class Unit:
    def __init__(self, side, x, y, power=3):
        self.hp = 200
        self.x = x
        self.y = y
        self.side = side
        self.power = power

    def __repr__(self):
        if self.side:
            return f'E({self.x}, {self.y}, {self.hp})'
        else:
            return f'G({self.x}, {self.y}, {self.hp})'

    def attack(self, units, grid):
        enemies = [(self.x-1,self.y),(self.x+1, self.y),(self.x,self.y-1),(self.x,self.y+1)]
        enemies = map(lambda x: grid[coord(*x)], enemies)
        enemies = filter(lambda x: isinstance(x, Unit) and x.side != self.side, enemies)
        enemies = list(sorted(enemies, key=lambda u: (u.hp, coord(u.x, u.y))))

        if not enemies:
            return False, None

        enemy = enemies[0]

        enemy.hp -= self.power
        if enemy.hp <= 0:
            grid[coord(enemy.x, enemy.y)] = None
            units.remove(enemy)
            return True, enemy
        return True, None

    def route(self, grid, px, py):
        # BFS
        visited = {(self.x, self.y): None}
        queue = deque(map(lambda x: (x, (self.x, self.y)), ranged(self.x, self.y, grid)))
        while queue:
            p, prev = queue.popleft()
            if p in visited:
                continue
            visited[p] = prev
            if p == (px, py):
                c = 1
                while visited[p] != (self.x, self.y):
                    c += 1
                    p = visited[p]
                return c, p[0], p[1]
            else:
                for r in ranged(p[0], p[1], grid):
                    if r not in visited:
                        queue.append((r, p))
        return None, None, None

    def move(self, units, grid):
        open_pos = []
        for u in units:
            if u.side != self.side:
                open_pos.extend(ranged(u.x, u.y, grid))
        routes = [r for r in map(lambda p: self.route(grid, *p), open_pos) if r[0] is not None]
        if not routes:
            return False
        r = min(routes, key=lambda x: (x[0], coord(x[1], x[2])))
        grid[coord(self.x, self.y)] = None
        _, self.x, self.y = r
        grid[coord(self.x, self.y)] = self
        return True

    def tick(self, units, grid) -> bool:
        # find targets
        tgs = [u for u in units if u.side != self.side]
        if not tgs:
            # end
            return True, None
        
        attacked, killed_unit = self.attack(units, grid)
        if attacked:
            return False, killed_unit
        
        # move
        if self.move(units, grid):
            attacked, killed_unit = self.attack(units, grid)
            if attacked:
                return False, killed_unit

        return False, None
        
def print_grid(grid, round):
    print('\n', round)
    for i, s in enumerate(grid):
        if i % cols == 0:
            print()
        if s is None:
            print('.', end="")
        elif s == WALL:
            print('#', end="")
        else:
            print('E' if s.side else 'G', end="")
        

WALL = -1

def init(attack_power=3):
    grid = [None] * rows * cols
    units = []
    for y, row in enumerate(in_lines):
        for x, c in enumerate(row):
            if c == '#':
                grid[coord(x, y)] = WALL
            elif c == 'G':
                u = Unit(False, x, y)
                units.append(u)
                grid[coord(x, y)] = u
            elif c == 'E':
                u = Unit(True, x, y, attack_power)
                units.append(u)
                grid[coord(x, y)] = u
    return grid, units

part1 = False

if part1:
    finished_rounds = 0
    grid, units = init(3)
    while True:
        not_moved = set(units)
        while not_moved:
            u = next_unit(not_moved)
            not_moved.remove(u)
            end, killed = u.tick(units, grid)
            if killed and killed in not_moved:
                not_moved.remove(killed)
            if end:
                s = sum(x.hp for x in units)
                print(finished_rounds, s, finished_rounds*s)
                sys.exit()
        finished_rounds += 1
        print(finished_rounds)
        #print_grid(grid, finished_rounds)
        #print(units)
else:
    elf_power = 3
    while True:
        print(elf_power)
        elf_power += 1
        grid, units = init(elf_power)
        finished_rounds = 0
        while True:
            not_moved = set(units)
            next_power = False
            while not_moved:
                u = next_unit(not_moved)
                not_moved.remove(u)
                end, killed = u.tick(units, grid)
                if killed and killed in not_moved:
                    not_moved.remove(killed)
                if killed and killed.side:
                    print('Elf killed')
                    next_power = True
                    break
                if end:
                    s = sum(x.hp for x in units)
                    print(finished_rounds, s, finished_rounds*s)
                    sys.exit()
            if next_power:
                break
            finished_rounds += 1
            print(elf_power, finished_rounds)
            #print_grid(grid, finished_rounds)
            #print(units)