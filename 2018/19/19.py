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
    4: 'addr',
    0: 'addi',
    15: 'mulr',
    6: 'muli',
    8: 'banr',
    7: 'bani',
    2: 'borr',
    12: 'bori',
    10: 'setr',
    5: 'seti',
    11: 'gtir',
    3: 'gtri',
    9: 'gtrr',
    14: 'eqir',
    13: 'eqri',
    1: 'eqrr'
}

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

def parse_program():
    ip_reg = 0
    ops = []
    for l in sys.stdin:
        if l[0] == '#':
            ip_reg = int(l.split(' ')[1])
        elif l.strip():
            parts = l.strip().split(' ')
            op = parts[0]
            opcode = 0
            op1, op2, target = int(parts[1]), int(parts[2]), int(parts[3])
            for opc, opn in OPCODENAMES.items():
                if opn == op:
                    opcode = opc
                    break
            ops.append((opcode, op1, op2, target))
    return ip_reg, ops

def part1(ip_reg, program):
    regs = [0] * 6
    ip = 0

    while 0 <= ip < len(program):
        regs[ip_reg] = ip
        run(regs, *program[ip])
        ip = regs[ip_reg]
        ip += 1

    print(regs)

def part2(ip_reg, program):
    regs = [1, 0, 0, 0, 0, 0]
    ip = 0

    while 0 <= ip < len(program):
        regs[ip_reg] = ip
        run(regs, *program[ip])
        ip = regs[ip_reg]
        ip += 1

    print(regs)

ip_reg, program = parse_program()
part1(ip_reg, program)
part2(ip_reg, program)