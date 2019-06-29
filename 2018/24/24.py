from dataclasses import dataclass, replace
import sys
import re

@dataclass
class Group:
    units: int
    unit_hp: int
    damage_amount: int
    damage_type: str
    initiative: int
    immunities: [str]
    weaknesses: [str]
    side: bool = False

    def __hash__(self):
        return self.initiative

    def powerup(self, powerup):
        return replace(self, damage_amount=self.damage_amount + powerup)

    def power(self):
        return self.units * self.damage_amount

    def damage_done(self, damage_type, power):
        if damage_type in self.immunities:
            return 0
        elif damage_type in self.weaknesses:
            return power * 2
        else:
            return power

    def select_target(self, candidates):
        candidates = filter(lambda x: x.side != self.side, candidates)
        top_damage = 0
        selected_targets = []
        for c in candidates:
            dam = c.damage_done(self.damage_type, self.power())
            if dam > top_damage:
                top_damage = dam
                selected_targets.clear()
            if dam == top_damage:
                selected_targets.append(c)

        if top_damage == 0:
            return None
        if len(selected_targets) > 1:
            #print('multiple candidates', selected_targets)
            c = max(selected_targets, key=lambda x: (x.power(), x.initiative))
            #print('using', c)
            return c
        return selected_targets[0]

    def attack(self, target):
        dam = target.damage_done(self.damage_type, self.power())
        target.units -= (dam // target.unit_hp)

immune_groups, infection_groups = [], []
active_groups = None

input_nums_regex = re.compile(r'(\d+)')
input_weak_regex = re.compile(r'weak to ([a-z, ]+)')
input_immune_regex = re.compile(r'immune to ([a-z, ]+)')
damage_type_regex = re.compile(r'(\w+) damage')

for l in sys.stdin:
    if not l.strip():
        continue
    if l.startswith('Immune'):
        active_groups = immune_groups
    elif l.startswith('Infection'):
        active_groups = infection_groups
    else:
        nums = [int(n) for n in input_nums_regex.findall(l)]
        weak_to = input_weak_regex.findall(l)
        if weak_to:
            weak_to = weak_to[0].split(', ')
        immune_to = input_immune_regex.findall(l)
        if immune_to:
            immune_to = immune_to[0].split(', ')
        damage_type = damage_type_regex.findall(l)[0]

        active_groups.append(Group(
            nums[0], nums[1], nums[2], damage_type, nums[3],
            immune_to, weak_to))

for g in immune_groups:
    g.side = True
groups = immune_groups + infection_groups

def select_targets(groups):
    targets_left: set = set(groups)
    groups.sort(key=lambda x: (-x.power(), -x.initiative))
    selected_targets = {}
    for g in groups:
        t = g.select_target(targets_left)
        if t is not None:
            selected_targets[g] = t
            targets_left.remove(t)

    return selected_targets

def attack_round(groups, selected_targets):
    groups.sort(key=lambda x: -x.initiative)
    for g in groups:
        if g not in selected_targets or g.units <= 0:
            continue
        t = selected_targets[g]
        g.attack(t)

    groups = [g for g in groups if g.units > 0]
    first_group_side = groups[0].side
    return groups, all(first_group_side == g.side for g in groups)

def run(immune, infection, powerup):
    immune = [g.powerup(powerup) for g in immune]
    groups = immune + [replace(g) for g in infection]
    iters_left = 10000
    while True:
        iters_left -= 1
        if iters_left <= 0:
            return None
        targets = select_targets(groups)
        if len(targets) == 0:
            return None
        groups, finished = attack_round(groups, targets)
        if finished:
            return groups

res1groups = run(immune_groups, infection_groups, 0)
print('1. ', sum(g.units for g in res1groups), res1groups[0].side)

max_failure, min_success = 0, 1000
while True:
    res_groups = run(immune_groups, infection_groups, min_success)
    if res_groups[0].side:
        break
    max_failure = min_success
    min_success += 1000
# binary search
while max_failure < min_success - 1:
    p = min_success + (max_failure - min_success) // 2
    res_groups = run(immune_groups, infection_groups, p)
    if not res_groups or not res_groups[0].side:
        max_failure = p
    else:
        min_success = p

print('2. ', min_success, '->', sum(g.units for g in run(immune_groups, infection_groups, min_success)))

