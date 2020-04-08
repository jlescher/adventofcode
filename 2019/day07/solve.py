#!/usr/bin/env python3

import argparse
import sys
import os
from itertools import permutations, chain, tee
from collections import deque
sys.path.append(os.path.dirname(os.getcwd()))
from day05 import solve as day05

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

class Intcode(day05.Intcode):
    def __init__(self, in_queue, out_queue, prog):
        super(Intcode, self).__init__()
        self.in_queue  = in_queue
        self.out_queue = out_queue
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
    queues = [ deque([p]) for p in permutation ]
    queues[0].appendleft(0)
    intcodes = [ Intcode(in_queue, out_queue, prog) for in_queue, out_queue in pairwise(chain(queues, [ queues[0] ])) ]
    
    while not intcodes[-1].halted:
        for x in intcodes:
            try:
                x.execute()
            except IndexError:
                pass
    return queues[0][0]

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
        



