import sys

rstr = sys.stdin.read().strip()
rounds = int(rstr)
rarr = list(map(int, rstr))

recipes = [3, 7]
elves = [0, 1]

while len(recipes) < rounds + 10:
    r0, r1 = recipes[elves[0]], recipes[elves[1]]
    s = r0 + r1
    if s >= 10:
        recipes.append(1)
    recipes.append(s % 10)

    elves[0] = (r0 + 1 + elves[0]) % len(recipes) 
    elves[1] = (r1 + 1 + elves[1]) % len(recipes) 

if len(recipes) == rounds + 11:
    recipes.pop()

print(''.join(map(str, recipes[-10:])))

# part 2
recipes = [3, 7]
elves = [0, 1]

for i in range(int(1e8)):
    r0, r1 = recipes[elves[0]], recipes[elves[1]]
    s = r0 + r1
    if s >= 10:
        recipes.append(1)
        if recipes[-len(rarr):] == rarr:
            print(len(recipes) - len(rarr))
            break
    recipes.append(s % 10)

    elves[0] = (r0 + 1 + elves[0]) % len(recipes) 
    elves[1] = (r1 + 1 + elves[1]) % len(recipes)

    if recipes[-len(rarr):] == rarr:
        print(len(recipes) - len(rarr))
        break
