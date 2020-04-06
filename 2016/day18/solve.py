#!/usr/bin/env python3


import argparse
from itertools import tee, chain
from pprint import pprint

example = '..^^.'

def threewise(iterable):
    "s -> (s0,s1, s2), (s1,s2, s3), (s2, s3, s4), ..."
    a, b, c = tee(chain('.', iterable, '.'), 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)

def get_row(r):
    new_r = []
    for l, c, r in threewise(r):
        if l == c == '^' and r == '.':
            new_r.append('^')
        elif c == r == '^' and l == '.':
            new_r.append('^')
        elif l == '^' and c == r == '.':
            new_r.append('^')
        elif l == c == '.' and r == '^':
            new_r.append('^')
        else:
            new_r.append('.')
    return ''.join(new_r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        l = f.read().strip()

    grid = [ l ]
    for _ in range(400000-1):
        grid.append(get_row(grid[-1]))

    # Fancy counter
    print('P1:', ''.join(grid[0:40]).count('.'))

    cnt = 0
    for r in grid:
        cnt += r.count('.')
    print('P2:', cnt)
    

