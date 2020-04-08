#!/usr/bin/env python3

import argparse
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from day05 import solve as day05
import logging

logging.basicConfig(level=logging.WARNING)

class Intcode(day05.Intcode):

    def __init__(self):
        super(Intcode, self).__init__()
        self.rel_base = 0
        
        self.read_param.update( { 2: { 'debug_str': 'r', 'func': lambda x: self.rel_base + self.memory[x] }})
        self.opcodes.update( { 9:  { 'param': 1, 'func': self.set_rel_base} })

    def set_rel_base(self, a):
        self.rel_base += self.memory[a]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = list(map(int, f.readline().split(',')))

    intcode = Intcode()
    intcode.reset_memory(prog)
    intcode.execute()
