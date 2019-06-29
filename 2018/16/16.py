import sys

ADDR=4
ADDI=0
MULR=15
MULI=6
BANR=8
BANI=7
BORR=2
BORI=12
SETR=10
SETI=5
GTIR=11
GTRI=3
GTRR=9
EQIR=14
EQRI=13
EQRR=1

OPCODENAMES = {
4: 'ADDR',
0: 'ADDI',
15: 'MULR',
6: 'MULI',
8: 'BANR',
7: 'BANI',
2: 'BORR',
12: 'BORI',
10: 'SETR',
5: 'SETI',
11: 'GTIR',
3: 'GTRI',
9: 'GTRR',
14: 'EQIR',
13: 'EQRI',
1: 'EQRR'}

def run(regs, opcode, operand1, operand2, target):
    if opcode == ADDR:
        regs[target] = regs[operand1] + regs[operand2]
    elif opcode == ADDI:
        regs[target] = regs[operand1] + operand2
    elif opcode == MULR:
        regs[target] = regs[operand1] * regs[operand2]
    elif opcode == MULI:
        regs[target] = regs[operand1] * operand2
    elif opcode == BANR:
        regs[target] = regs[operand1] & regs[operand2]
    elif opcode == BANI:
        regs[target] = regs[operand1] & operand2
    elif opcode == BORR:
        regs[target] = regs[operand1] | regs[operand2]
    elif opcode == BORI:
        regs[target] = regs[operand1] | operand2
    elif opcode == SETR:
        regs[target] = regs[operand1]
    elif opcode == SETI:
        regs[target] = operand1
    elif opcode == GTIR:
        regs[target] = 1 if operand1 > regs[operand2] else 0
    elif opcode == GTRI:
        regs[target] = 1 if regs[operand1] > operand2 else 0
    elif opcode == GTRR:
        regs[target] = 1 if regs[operand1] > regs[operand2] else 0
    elif opcode == EQIR:
        regs[target] = 1 if operand1 == regs[operand2] else 0
    elif opcode == EQRI:
        regs[target] = 1 if regs[operand1] == operand2 else 0
    elif opcode == EQRR:
        regs[target] = 1 if regs[operand1] == regs[operand2] else 0

def part1():
    with open('in_1.txt') as f:
        in_lines = [l.strip() for l in f.readlines() if l.strip()]
    samples = 0
    for i in map(lambda x: x*3, range(len(in_lines)//3)):
        regs_before = list(map(int, in_lines[i][9:-1].split(', ')))
        regs_after = list(map(int, in_lines[i+2][9:-1].split(', ')))
        op = list(map(int, in_lines[i+1].split(' ')))

        c = 0
        for opcode in range(16):
            regs = regs_before[:]
            run(regs, opcode, *op[1:])
            if regs_after == regs:
                c += 1
                if c >= 3:
                    samples += 1
                    break
    print(samples)

def opcodefind():
    with open('in_1.txt') as f:
        in_lines = [l.strip() for l in f.readlines() if l.strip()]
    known = {}
    while len(known) < 16:
        for i in map(lambda x: x*3, range(len(in_lines)//3)):
            regs_before = list(map(int, in_lines[i][9:-1].split(', ')))
            regs_after = list(map(int, in_lines[i+2][9:-1].split(', ')))
            op = list(map(int, in_lines[i+1].split(' ')))

            if op[0] in known:
                continue

            opcode_candidates = set()
            for opcode in range(16):
                if opcode in known.values():
                    continue
                regs = regs_before[:]
                run(regs, opcode, *op[1:])
                if regs_after == regs:
                    opcode_candidates.add(opcode)
            if len(opcode_candidates) == 1:
                correct_opcode = opcode_candidates.pop()
                print(op[0], '=', OPCODENAMES[correct_opcode])
                known[op[0]] = correct_opcode
    print(known)

def opcodetest():
    with open('in_1.txt') as f:
        in_lines = [l.strip() for l in f.readlines() if l.strip()]
    for i in map(lambda x: x*3, range(len(in_lines)//3)):
        regs_before = list(map(int, in_lines[i][9:-1].split(', ')))
        regs_after = list(map(int, in_lines[i+2][9:-1].split(', ')))
        op = list(map(int, in_lines[i+1].split(' ')))

        regs = regs_before[:]
        run(regs, *op)
        if regs_after != regs:
            print("ERROR", op, regs_before, "->", regs, "!=", regs_after)

def part2():
    with open('in_2.txt') as f:
        instructions = [[int(x) for x in l.strip().split(' ')] for l in f.readlines() if l.strip()]
    regs = [0, 0, 0, 0]
    for i in instructions:
        run(regs, *i)
    print(regs)

part1()
opcodefind()
opcodetest()
part2()