#!/usr/bin/env python3


def cpy(ip, regs, x, y):
    if x in 'abcd':
        x = regs[x]
    else:
        x = int(x)

    regs[y] = x
    return ip + 1


def inc(ip, regs, a):
    regs[a] += 1
    return ip + 1


def dec(ip, regs, a):
    regs[a] -= 1
    return ip + 1


def jnz(ip, regs, x, y) -> int:
    if x in 'abcd':
        x = regs[x]
    else:
        x = int(x)
    y = int(y)

    if x != 0:
        return ip + y
    else:
        return ip + 1


def main():
    regs1 = { 'a': 0, 'b': 0, 'c': 0, 'd': 0 }
    regs2 = { 'a': 0, 'b': 0, 'c': 1, 'd': 0 }
    instructions1 = []
    instructions2 = []
    ip = 0

    with open('input.txt') as f:
        for line in f:
            if line.startswith('cpy'):
                func = cpy
            elif line.startswith('inc'):
                func = inc
            elif line.startswith('dec'):
                func = dec
            elif line.startswith('jnz'):
                func = jnz
            elif not line.isspace():
                print("Invalid line", line)
                return

            instructions1.append((func, [regs1] + line.split()[1:]))
            instructions2.append((func, [regs2] + line.split()[1:]))

    while ip < len(instructions1):
        ins = instructions1[ip]
        ip = ins[0](ip, *ins[1])

    ip = 0
    while ip < len(instructions2):
        ins = instructions2[ip]
        ip = ins[0](ip, *ins[1])

    print("Part 1:", regs1)
    print("Part 2:", regs2)

main()
