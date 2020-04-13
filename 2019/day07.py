#!/usr/bin/env python3

import argparse
from itertools import permutations
from lib.intcode import VM
import pdb, pudb


# Poor man's scheduler
def run(permutation, exe):
    vms = [ VM(exe) for _ in permutation ]

    # Push in the permutation
    for vm, p in zip(vms, permutation):
        vm.push_in(p)

    # Send signal to the vm
    vms[0].push_in(0)

    #
    # Run the poor man's scheduler, as soon as an output is produced, manually
    # push it to the next vm.
    #
    # Therefore we are resilient to the case where:
    #     - last vm is waiting for a single input
    #     - vm before last sent the input and entered an infinite loop
    #

    conn = None # connection between the vms
    out = 0     # running output of last vm

    while not vms[1].is_halted():
        for vm in vms:
            # Push the previous connput
            if conn is not None:
                vm.push_in(conn)
                conn = None
            try:
                conn = next(vm.run())
                if vm == vms[-1] and conn is not None:
                    out = conn
            except StopIteration: # vm halted 
                pass
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
