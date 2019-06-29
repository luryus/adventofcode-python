
import sys
from collections import deque

init_state_str = sys.stdin.readline().strip().split(" ")[-1]
init_state = map(lambda x: 1 if x == '#' else 0, init_state_str)
leftmost_idx = 0
state = list(init_state)

rules = (l.strip().split(' => ') for l in sys.stdin.readlines() if not l.isspace())
rules = [list(map(lambda x: 1 if x == '#' else 0, l[0])) for l in rules if l[1] == '#']
rule_len = len(rules[0])
rules.sort()

# pad
leftmost_idx -= (rule_len - 1) 
state = [0] * (rule_len - 1) + state
state.extend([0] * (rule_len - 1))

seen = {}
seen[(''.join(map(str, state)))] = 0, leftmost_idx

gens = 50000000000
for g in range(gens):
    if g == 20:
        print(sum(i + leftmost_idx for (i, v) in enumerate(state) if v == 1))
    #print(g+1, ''.join('#' if s == 1 else '.' for s in state))
    next_state = list()
    # pad
    next_state.extend([0] * (rule_len // 2))

    last_1 = 0
    first_1 = None
    for i in range(len(state) - (rule_len - 1)):
        sslice = state[i:i+rule_len] 
        for r in rules:
            if sslice == r:
                next_state.append(1)
                if first_1 is None:
                    first_1 = i
                last_1 = i
                break
            elif sslice > r:
                continue
        else:
            next_state.append(0)
    
    if first_1 + (rule_len // 2) < rule_len - 1:
        next_state = ([0] * (rule_len - 1 - first_1 - (rule_len // 2))) + next_state
        leftmost_idx -= (rule_len - 1 - first_1 - (rule_len // 2))
    while last_1 + (rule_len // 2) > (len(next_state) - (rule_len)):
        next_state.append(0)

    # unpad
    while all(s == 0 for s in next_state[:5]):
        leftmost_idx += 1
        next_state.pop(0)
    while all(s == 0 for s in next_state[-5:]):
        next_state.pop()

    if (''.join(map(str, next_state))) in seen:
        prev_i, prev_offset = seen[(''.join(map(str, next_state)))]
        print("REPEAT", prev_i, g, prev_offset, leftmost_idx)
        round_diff = g - prev_i
        idx_diff = leftmost_idx - prev_offset

        leftmost_idx = (gens - g - 1) * idx_diff + leftmost_idx
        state = next_state
        break

    seen[(''.join(map(str, next_state)))] = i, leftmost_idx

    state = next_state


print(sum(i + leftmost_idx for (i, v) in enumerate(state) if v == 1))