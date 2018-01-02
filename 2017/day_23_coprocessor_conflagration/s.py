#!/usr/bin/env python3

cnt_mul = 0
regs = {'a': 1}

def get_val(y):
    try:
        return int(y)
    except ValueError:
        return regs.get(y, 0)

def set_(x, y, line):
    y = get_val(y)
    regs[x] = y
    return line+1

def sub(x, y, line):
    y = get_val(y)
    regs[x] = regs.get(x, 0) - y
    return line+1

def mul(x, y, line):
    global cnt_mul
    y = get_val(y)
    regs[x] = regs.get(x, 0) * y
    cnt_mul += 1
    return line+1

def jnz(x, y, line):
    x = get_val(x)
    if x != 0:
        return line + get_val(y)
    else:
        return line+1


ins = {
        'set': set_,
        'sub': sub,
        'mul': mul,
        'jnz': jnz,
        }

with open('input') as f:
    prog = [x.rstrip().split() for x in f.readlines() ]
    print(prog)

    line = 0
    while 0 <= line < len(prog):
        a = prog[line]
        line = ins[prog[line][0]](*prog[line][1:], line)
    print(cnt_mul)



