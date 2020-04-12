#!/usr/bin/env python3

import argparse
from collections import deque
from itertools import permutations
from lib.intcode import VM


# Poor man's scheduler
def run(permutation, exe):
    vms = [ VM(exe) for _ in permutation ]

    # Connect the vms (out[i] -> input[i+1]) in daisy chain
    for i in range(len(vms)):
        vms[i].register_stream_func(vms[(i+1) % len(vms)].push_in)

    # Push in the permutation
    for vm, p in zip(vms, permutation):
        vm.push_in(p)

    # Push in the signal 0
    vms[0].push_in(0)

    # Run the poor man's scheduler
    while not vms[-1].halted:
        for vm in vms:
            out = vm.run()
    return out

def part1(exe):
    return max(run(p, exe) for p in permutations(range(5)))

def part2(exe):
    return max(run(p, exe) for p in permutations(range(5, 10)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        exe = list(map(int, f.readline().split(',')))

    print('part1: {}'.format(part1(exe)))
    print('part2: {}'.format(part2(exe)))
