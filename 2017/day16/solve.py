#!/usr/bin/env python3

import string
from collections import deque

LOOPS = 1000000000

def spin(p, s):
    p.rotate(int(s))

def exchange(p, s):
    m, n = map(int, s.split('/'))
    p[m], p[n] = p[n], p[m]

def partner(p, s):
    m, n = map(p.index, s.split('/'))
    p[m], p[n] = p[n], p[m]

switchcase = {
        's': spin,
        'x': exchange,
        'p': partner
        }

def dance(programs, stream):
    for ins in stream.rstrip().rstrip(',').split(','):
        switchcase[ins[0]](programs, ins[1:])

with open('input') as f:
    known_states = []
    programs = deque(string.ascii_lowercase[0:16])
    known_states.append(programs.copy())
    moves = f.read()
    for i in range(LOOPS):
        print(i)
        dance(programs, moves)
        if programs not in known_states:
            known_states.append(programs.copy())
        else:
            ix = known_states.index(programs)
            loop_size = len(known_states) - ix
            print(''.join(known_states[ix + ((LOOPS - ix) % loop_size)]))
            break
