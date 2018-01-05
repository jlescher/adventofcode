#!/usr/bin/env python3

def simple_increase(steps):
    ix = 0
    cnt = 0
    while 0 <= ix < len(steps):
        cnt += 1
        inc = steps[ix]
        steps[ix] += 1
        ix += inc
    return cnt

def not_so_simple_increase(steps):
    ix = 0
    cnt = 0
    while 0 <= ix < len(steps):
        cnt += 1
        inc = steps[ix]
        if inc  >= 3:
            steps[ix] -= 1
        else:
            steps[ix] += 1
        ix += inc
    return cnt

with open('input') as f:
    steps = [ int(x.rstrip()) for x in f.readlines() ]
    print('P1:', simple_increase(steps[:]))
    print('P2:', not_so_simple_increase(steps[:]))

