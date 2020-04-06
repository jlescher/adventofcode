#!/usr/bin/env python3

import z3
import operator
import argparse
import re
import pdb

def get_manhattan_distance(here, there):
    return sum( map(abs, map(operator.sub, here, there)))

def part1(nanobots):
    max_nanobot = max(nanobots, key=lambda x:x[-1])
    return len( [ x for x in nanobots if get_manhattan_distance(x[:-1], max_nanobot[:-1]) <= max_nanobot[-1] ] )

def count_inrange_nanobots(pos, nanobots):
    return len( [ x for x in nanobots if get_manhattan_distance(x[:-1], pos) <= x[-1] ] )

def z3_abs(x):
    return z3.If(x > 0, x, -x)

def part2(nanobots):
    x, y, z = z3.Int('x'), z3.Int('y'), z3.Int('z')
    in_range = [ z3.Int('in_range_{}'.format(i)) for i in range(len(nanobots)) ]
    cnt = z3.Int('cnt')
    dist = z3.Int('dist')
    opt = z3.Optimize()
    for ni, eqi in zip(nanobots, in_range):
        opt.add(eqi == z3.If( z3_abs(ni[0] - x) + z3_abs(ni[1] - y) + z3_abs(ni[2] - z) <= ni[3], 1, 0))
    opt.add(cnt == sum(in_range))
    opt.add(dist == z3_abs(x) + z3_abs(y) + z3_abs(z) )
    opt.maximize(cnt)
    opt.minimize(dist)
    opt.check()
    return opt.model()[dist]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        nanobots = [ tuple(map(int, re.findall(r'-?\d+', x))) for x in f.readlines() ]

    print('part1: {}'.format(part1(nanobots)))
    print('part2: {}'.format(part2(nanobots)))
