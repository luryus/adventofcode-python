#!/usr/bin/env python3

from itertools import cycle


output = []


def cpy(ip, regs, progr, x, y):
    if y in 'abcd':
        if x in 'abcd':
            x = regs[x]
        else:
            x = int(x)

        regs[y] = x
    return ip + 1


def inc(ip, regs, progr, a):
    if a in 'abcd':
        regs[a] += 1
    return ip + 1


def dec(ip, regs, progr, a):
    if a in 'abcd':
        regs[a] -= 1
    return ip + 1


def jnz(ip, regs, progr, x, y) -> int:
    if x in 'abcd':
        x = regs[x]
    else:
        x = int(x)
    if y in 'abcd':
        y = regs[y]
    else:
        y = int(y)

    if x != 0:
        return ip + y
    else:
        return ip + 1


def tgl(ip, regs, progr: [tuple], x) -> int:
    if x in 'abcd':
        x = regs[x]
    else:
        x = int(x)

    if ip + x < 0 or ip + x >= len(progr):
        return ip + 1

    if progr[ip + x][0] in (dec, tgl):
        func = inc
    elif progr[ip + x][0] == inc:
        func = dec
    elif progr[ip + x][0] == cpy:
        func = jnz
    else:
        func = cpy
    progr[ip + x] = (func,) + progr[ip + x][1:]

    return ip + 1


def out(ip, regs, progr: [tuple], x) -> int:
    if x in 'abcd':
        x = regs[x]
    else:
        x = int(x)

    output.append(x)

    return ip + 1


def main():
    instructions = []
    regs = {}

    with open('input.txt') as f:
        for line in f:
            func = None
            if line.startswith('cpy'):
                func = cpy
            elif line.startswith('inc'):
                func = inc
            elif line.startswith('dec'):
                func = dec
            elif line.startswith('jnz'):
                func = jnz
            elif line.startswith('tgl'):
                func = tgl
            elif line.startswith('out'):
                func = out
            elif not line.isspace():
                print("Invalid line", line)
                return

            instructions.append(
                (func, (regs, instructions) + tuple(line.split()[1:])))

    init_a = 0
    while True:
        # find first number divisible by 4 which is successful
        regs['a'] = init_a
        ip = 0
        output.clear()

        while ip < len(instructions):
            if ip == 3:
                # optimization for my input, probably won't work for all
                regs['d'] += regs['b'] * regs['c']
                ip = 8
                continue

            if ip == 10:
                regs['c'] = regs['a'] % 2
                if regs['c'] == 0:
                    regs['c'] = 2
                regs['a'] //= 2
                ip = 20
                continue

            if ip == 20:
                regs['b'] = 2 - regs['c']
                regs['c'] = 0
                ip = 26
                continue

            ins = instructions[ip]
            ip = ins[0](ip, *ins[1])

            if ins[0] == out:
                if output[-1] != (len(output) - 1) % 2:
                    break
                elif len(output) > 10000:
                    print("Smallest value: ", init_a)
                    return

        init_a += 4


main()
