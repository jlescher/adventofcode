#!/usr/bin/env python3

import argparse
import logging
from collections import defaultdict
from itertools import count

class Intcode:

    def __init__(self):
        self.pc = 0
        self.inc_pc  = True
        self.halted  = False
        self.opcodes = {
                1:  { 'param': 3, 'func': self.add},
                2:  { 'param': 3, 'func': self.mul},
                3:  { 'param': 1, 'func': self._input},
                4:  { 'param': 1, 'func': self.output},
                5:  { 'param': 2, 'func': self.jump_if_true},
                6:  { 'param': 2, 'func': self.jump_if_false},
                7:  { 'param': 3, 'func': self.less_than},
                8:  { 'param': 3, 'func': self.equal},
                99: { 'param': 0, 'func': self.halt},
                }

        self.read_param = {
                0: { 'debug_str': 'p', 'func': lambda x: self.memory[x] },
                1: { 'debug_str': 'i', 'func': lambda x: x },
                }

    def add(self, a, b, c):
        self.memory[c] = self.memory[a] + self.memory[b]

    def mul(self, a, b, c):
        self.memory[c] = self.memory[a] * self.memory[b]

    def _input(self, a):
        self.memory[a] = int(input('Please send input: '))

    def output(self, a):
        print(self.memory[a])

    def jump_if_true(self, a, b):
        if self.memory[a]:
            self.inc_pc = False
            self.pc = self.memory[b]

    def jump_if_false(self, a, b):
        if not self.memory[a]:
            self.inc_pc = False
            self.pc = self.memory[b]

    def less_than(self, a, b, c):
        if self.memory[a] < self.memory[b]:
            self.memory[c] = 1
        else:
            self.memory[c] = 0

    def equal(self, a, b, c):
        if self.memory[a] == self.memory[b]:
            self.memory[c] = 1
        else:
            self.memory[c] = 0

    def halt(self):
        self.halted = True

    def reset_memory(self, prog):
        self.memory = defaultdict(int)
        for i, j in enumerate(prog):
            self.memory[i] = j

    def get_modes(self, raw_opcode, num_params):
        raw_opcode //=100
        modes = []
        # Can we write that loop as a list comprehension
        for i in range(num_params):
            modes.append(raw_opcode % 10)
            raw_opcode //=10
        return modes

    def execute_instruction(self):
        # Fetch and decode opcode 
        raw_opcode = self.memory[self.pc]
        opcode = raw_opcode % 100
        num_params = self.opcodes[opcode]['param']

        # Fetch and decode instruction
        modes = self.get_modes(raw_opcode, num_params)
        params = [ self.read_param[mode]['func'](addr) for mode, addr in zip(modes, count(self.pc + 1)) ]

        # Logging 
        instruction = [ self.memory[x] for x in range(self.pc, self.pc + num_params + 1) ]
        logging.debug('-'*80)
        logging.debug('pc: ' + str(self.pc))
        try:
            logging.debug('rel_base: ' + str(self.rel_base))
        except AttributeError:
            pass
        logging.debug('raw  instruction: ' + '{:12d}  '.format(instruction[0])                        +  ''.join(map( lambda x: ' {:4d}'.format(x), instruction[1:])))
        logging.debug('dec  instruction: ' + '{:>12s}  '.format(self.opcodes[opcode]['func'].__name__) + ''.join(map( lambda x: ' {:>4s}'.format(x),  map( lambda x, y: self.read_param[x]['debug_str'] + str(y), modes, instruction[1:]))))
        logging.debug('mem  instruction: ' + '{:>12s}  '.format(self.opcodes[opcode]['func'].__name__) + ''.join(map( lambda x: ' {:4d}'.format(self.memory[x]), params)))


        # Execute
        self.inc_pc = True # increment pc by default unless the instruction marks the pc as already incremented
        self.opcodes[opcode]['func'](*params)
        logging.debug('mem  instruction: ' + '{:>12s}  '.format(self.opcodes[opcode]['func'].__name__) + ''.join(map( lambda x: ' {:4d}'.format(self.memory[x]), params)))

        # Move pc
        if self.inc_pc:
            self.pc += 1 + self.opcodes[opcode]['param']

    def execute(self):
        while not self.halted:
            self.execute_instruction()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = list(map(int, f.readline().split(',')))

    intcode = Intcode()
    intcode.reset_memory(prog)
    intcode.execute()

