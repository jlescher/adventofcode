#!/usr/bin/env python3

import argparse
import sys
import os
from itertools import permutations
sys.path.append(os.path.dirname(os.getcwd()))
from day05 import solve as day05


class Intcode(day05.Intcode):
    def __init__(self, setting, signal, prog):
        super(Intcode, self).__init__()
        self.input_queue = [ signal, setting ]
        self.opcodes[3] = { 'param': 1, 'func': self._input}
        self.opcodes[4] = { 'param': 1, 'func': self.output}
        self.reset_memory(prog)

    def _input(self, a):
        self.memory[a] = self.input_queue.pop()

    def output(self, a):
        self.output = self.memory[a]

def run(permutation, prog):
    signal = 0
    for e in permutation:
        intcode = Intcode(e, signal, prog)
        intcode.execute()
        signal = intcode.output
    return signal

def part1(prog):
    return max(run(p, prog) for p in permutations(range(5)))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = list(map(int, f.readline().split(',')))

    print('part1: {}'.format(part1(prog)))
        



