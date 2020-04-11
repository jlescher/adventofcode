#!/usr/bin/env python3

import argparse, sys, os
from itertools   import permutations
from collections import deque
sys.path.append(os.path.dirname(os.getcwd()))
from day05 import solve as day05

class VM(day05.VM):
    def __init__(self, prog):
        super(VM, self).__init__()
        self.opcodes.update( {
            3: { 'param': 1, 'func': self._input},
            4: { 'param': 1, 'func': self.output}
            } )
        self.reset_memory(prog)

    def _input(self, a):
        self.memory[a] = self.in_queue.pop()

    def output(self, a):
        self.out_queue.appendleft(self.memory[a])

# Poor man's threading
def run(permutation, prog):
    pipes = [ deque([i]) for i in permutation ]
    vms =   [ VM(prog) for _ in permutation ]

    # Connect the vms
    for pipe, vm in zip(pipes, vms):
        vm.in_queue = pipe
    for i in range(len(vms) - 1):
        vms[i].out_queue = vms[i+1].in_queue
    vms[-1].out_queue = vms[0].in_queue

    # Send signal to first vm
    vms[0].in_queue.appendleft(0)
    
    while not vms[-1].halted:
        for vm in vms:
            try:
                vm.execute()
            except IndexError:
                pass

    return vms[-1].out_queue.pop()


def part1(prog):
    return max(run(p, prog) for p in permutations(range(5)))

def part2(prog):
    return max(run(p, prog) for p in permutations(range(5, 10)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = list(map(int, f.readline().split(',')))

    print('part1: {}'.format(part1(prog)))
    print('part2: {}'.format(part2(prog)))
