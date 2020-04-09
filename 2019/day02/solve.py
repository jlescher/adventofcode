#!/usr/bin/env python3

import argparse
import logging
from collections import defaultdict

logging.basicConfig(level=logging.WARNING)

class VM:
    def __init__(self):
        self.pc = 0
        self.run  = True
        self.opcodes = {
                1: self.add,
                2: self.mul,
                99: self.halt,
                }

    def add(self):
        self.memory[self.memory[self.pc+3]] = self.memory[self.memory[self.pc+1]] + self.memory[self.memory[self.pc+2]]
        self.pc += 4

    def mul(self):
        self.memory[self.memory[self.pc+3]] = self.memory[self.memory[self.pc+1]] * self.memory[self.memory[self.pc+2]]
        self.pc += 4

    def halt(self):
        self.run = False

    def reset_memory(self, prog):
        self.memory = defaultdict(int)
        for i, j in enumerate(prog):
            self.memory[i] = j

    def execute(self):
        self.pc = 0
        self.run = True
        while self.run:
            logging.info(self)
            self.opcodes[self.memory[self.pc]]()

    def __str__(self):
        if not self.memory:
            return 'VM not initialized yet'

        s = ''
        for i in range(max(self.memory)+1):
            s += str(self.memory[i]) + ','
        return s

def run_noun_verb(noun, verb, prog):
    vm.reset_memory(prog)
    vm.memory[1] = noun
    vm.memory[2] = verb
    vm.execute()
    return vm.memory[0]

def part1(prog):
    return run_noun_verb(12, 2, prog)

def part2(prog):
    for noun in range(100):
        for verb in range(100):
            logging.info('noun:{} verb:{}'.format(noun, verb))
            if run_noun_verb(noun, verb, prog) == 19690720:
                return 100*noun + verb

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = list(map(int, f.readline().split(',')))

    vm = VM()
    print('part1: {}'.format(part1(prog)))
    print('part2: {}'.format(part2(prog)))
        

        


