#!/usr/bin/env python3

registers = {}

def get_val(v):
    try:
        return int(v)
    except ValueError:
        return registers.get(v, 0)

with open('input') as f:
    prog = f.readlines()
    prog = [ x.rstrip().split() for x in prog ]
    # There are no jump instruction so it is safe to read one line after the other
    running_max = 0
    for l in prog:
        cond0 = get_val(l[4])
        cond1 = get_val(l[6])
        if eval('{} {} {}'.format(cond0, l[5], cond1)):
            op = 1 if l[1] == 'inc' else -1
            registers[l[0]] = get_val(l[0]) + (op * get_val(l[2]))
            running_max = max(running_max, registers[l[0]])
    print('P1:', max(registers.values()))
    print('P2:', running_max)
