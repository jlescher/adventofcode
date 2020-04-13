#!/usr/bin/env python2

import logging
from collections import defaultdict, deque
import pdb, pudb

#logging.basicConfig(level=logging.DEBUG)

class VM:
    '''
    Incode VM
    '''

    def __init__(self, exe=[]):
        self.pc = 0
        self.rel_base = 0
        self.halted  = False
        self.in_queue = deque([])
        self.out = None
        self.reset_memory(exe)

        # Internals
        self.inc_pc  = None         # updated by jump instruction to skip pc increment

        self.opcodes = {
                1:  { 'param': 3, 'func': self.add},
                2:  { 'param': 3, 'func': self.mul},
                3:  { 'param': 1, 'func': self.input},
                4:  { 'param': 1, 'func': self.output},
                5:  { 'param': 2, 'func': self.jump_if_true},
                6:  { 'param': 2, 'func': self.jump_if_false},
                7:  { 'param': 3, 'func': self.less_than},
                8:  { 'param': 3, 'func': self.equal},
                9:  { 'param': 1, 'func': self.set_rel_base},
                99: { 'param': 0, 'func': self.halt},
                }

        self.read_param = {
                0: { 'debug_str': 'p', 'func': lambda x: self.memory[x] },
                1: { 'debug_str': 'i', 'func': lambda x: x },
                2: { 'debug_str': 'r', 'func': lambda x: self.rel_base + self.memory[x] },
                }

        self.gen = self._run()

    def add(self, a, b, c):
        self.memory[c] = self.memory[a] + self.memory[b]

    def mul(self, a, b, c):
        self.memory[c] = self.memory[a] * self.memory[b]

    def input(self, a): # Name overrides the input build-in but we dont't care
        try:
            self.memory[a] = self.in_queue.pop()
        except IndexError:
            # input queue is empty
            # try to capture input
            inp = yield
            if inp == None:
                self.inc_pc = False
            else:
                self.push_in(inp)

    def output(self, a):
        yield self.memory[a]

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

    def set_rel_base(self, a):
        self.rel_base += self.memory[a]

    def halt(self):
        self.halted = True

    def execute_instruction(self):
        # Fetch and decode opcode
        raw_opcode = self.memory[self.pc]
        opcode , raw_opcode = raw_opcode % 100, raw_opcode // 100
        n_param = self.opcodes[opcode]['param']

        # Fetch and decode instruction params
        modes = []  # mode of the param, needed for debugging
        params = [] # memory address of the effective param
        for addr in range(self.pc + 1, self.pc + 1 + n_param):
                mode , raw_opcode = raw_opcode % 10, raw_opcode // 10
                param = self.read_param[mode]['func'](addr)
                modes.append(mode)
                params.append(param)

        # Logging 
        if opcode == 99:
            pass
        instruction = [ self.memory[x] for x in range(self.pc, self.pc + n_param + 1) ]
        logging.debug('-'*80)
        logging.debug('pc: ' + str(self.pc))
        logging.debug('rel_base: ' + str(self.rel_base))
        logging.debug('raw  instruction: ' + '{:12d}  '.format(instruction[0])                        + ''.join(map( lambda x: ' {:4d}'.format(x), instruction[1:])))
        logging.debug('dec  instruction: ' + '{:>12s} '.format(self.opcodes[opcode]['func'].__name__) + ''.join(map( lambda x: ' {:>4s}'.format(x),  map( lambda x, y: self.read_param[x]['debug_str'] + str(y), modes, instruction[1:]))))
        logging.debug('mem  instruction: ' + '{:>12s} '.format(self.opcodes[opcode]['func'].__name__) + ''.join(map( lambda x: ' {:4d}'.format(self.memory[x]), params)))

        # Execute
        self.inc_pc = True # by default: increment pc
        if opcode in (3, 4):
            yield from self.opcodes[opcode]['func'](*params)
        else:
            self.opcodes[opcode]['func'](*params)

        # Logging after execution
        logging.debug('mem  instruction: ' + '{:>12s} '.format(self.opcodes[opcode]['func'].__name__) + ''.join(map( lambda x: ' {:4d}'.format(self.memory[x]), params)))

        # Move pc
        if self.inc_pc:
            self.pc += 1 + n_param

    def reset_memory(self, prog):
        self.memory = defaultdict(int)
        for i, j in enumerate(prog):
            self.memory[i] = j

    def push_in(self, *args):
        for a in args:
            self.in_queue.appendleft(a)

    def _run(self):
        '''
        Generator that yields each output as soon as it can.
        Runs until VM is halted.
        '''
        while not self.halted:
            yield from self.execute_instruction()

    def run(self, *args):
        self.push_in(*args)
        return self.gen
    
    def is_halted(self):
        return self.halted
