#!/usr/bin/env python3


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


def main():
    regs = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
    instructions = []
    ip = 0

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
            elif not line.isspace():
                print("Invalid line", line)
                return

            instructions.append(
                (func, (regs, instructions) + tuple(line.split()[1:])))

    counter = 0
    while ip < len(instructions):
        counter += 1
        ins = instructions[ip]
        ip = ins[0](ip, *ins[1])

    print("Part 1:", regs)


main()
