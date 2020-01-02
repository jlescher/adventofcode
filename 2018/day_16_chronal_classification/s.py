#!/usr/bin/env python3

import argparse
import re
from pprint import pprint
from copy   import deepcopy

class Device:
    def __init__(self):
        self.registers = [ 0 for i in range(4) ]
        self.instructions = [
                self.addr,
                self.addi,
                self.mulr,
                self.muli,
                self.banr,
                self.bani,
                self.borr,
                self.bori,
                self.setr,
                self.seti,
                self.gtir,
                self.gtri,
                self.gtrr,
                self.eqir,
                self.eqri,
                self.eqrr,
                ]

    def execute_prog(self, prog):
        self.set_registers(0, 0, 0, 0)
        print(self.registers)
        if self.opcodes:
            for opcode, A, B, C in prog:
                print(self.opcodes[opcode].__name__, '(', A, B, C, ')')
                self.opcodes[opcode](A, B, C)
                print(self.registers)

    def set_registers(self, A, B, C, D):
        self.registers = [ A, B, C, D ]

    def addr(self, A, B, C):
        self.registers[C] = self.registers[A] + self.registers[B]

    def addi(self, A, B, C):
        self.registers[C] = self.registers[A] + B

    def mulr(self, A, B, C):
        self.registers[C] = self.registers[A] * self.registers[B]

    def muli(self, A, B, C):
        self.registers[C] = self.registers[A] * B

    def banr(self, A, B, C):
        self.registers[C] = self.registers[A] & self.registers[B]

    def bani(self, A, B, C):
        self.registers[C] = self.registers[A] & B

    def borr(self, A, B, C):
        self.registers[C] = self.registers[A] | self.registers[B]

    def bori(self, A, B, C):
        self.registers[C] = self.registers[A] | B

    def setr(self, A, B, C):
        self.registers[C] = self.registers[A]

    def seti(self, A, B, C):
        self.registers[C] = A

    def gtir(self, A, B, C):
        self.registers[C] = 1 if A > self.registers[B] else 0

    def gtri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > B else 0

    def gtrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > self.registers[B] else 0

    def eqir(self, A, B, C):
        self.registers[C] = 1 if A == self.registers[B] else 0

    def eqri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == B else 0

    def eqrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == self.registers[B] else 0

    def map_instructions_to_opcodes(self, tests):
        # Create a set for each opcode number
        opcodes = [ set(self.instructions) for i in range(16)] 
        for t in tests:
            opcode = t[1][0]
            is_valid = set()
            for instruction in opcodes[opcode]:
                self.set_registers(*t[0])
                instruction(*t[1][1:])
                if tuple(self.registers) == t[2]:
                    is_valid.add(instruction)
            opcodes[opcode] = is_valid

        # Map unique opcodes and remove them from the other sets
        self.opcodes = [ None for i in range(16) ]
        while True:
            found = False
            # Loop through the sets and add unambiguous opcodes 
            for opcode, instructions in enumerate(opcodes):
                if len(instructions) == 1:
                    instruction = instructions.pop()
                    self.opcodes[opcode] = instruction
                    found = True
                    break
            # Remove instructions[1] from the other sets
            if found:
                for instructions in opcodes:
                    instructions.discard(instruction)
            else:
                break
        assert len(set(self.opcodes)) == len(self.opcodes)

def part1(tests):
    d = Device()
    cnt = 0
    for t in tests:
        cnt_i = 0
        for instruction in d.instructions:
            d.set_registers(*t[0])
            instruction(*t[1][1:])
            if tuple(d.registers) == t[2]:
                cnt_i += 1
        if cnt_i >= 3:
            cnt += 1
    return cnt

def part2(tests, prog):
    d = Device()
    d.map_instructions_to_opcodes(tests)
    d.execute_prog(prog)
    return d.registers[0]
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        lines = f.readlines()

    # Extract part1 input
    i = 0
    tests = []
    regexp = re.compile(r'\d+')
    try:
        while 'Before' in lines[i]:
            before      = map(int, regexp.findall(lines[i]))
            instruction = map(int, regexp.findall(lines[i+1]))
            after       = map(int, regexp.findall(lines[i+2]))
            tests.append((tuple(before), tuple(instruction), tuple(after)))
            i += 4
    except IndexError:
        pass
    
    # Extract part2 input
    prog = [ tuple(map(int, l.strip().split(' '))) for l in lines[i+2:] ]

    print('part1: {}'.format(part1(tests)))
    print('part2: {}'.format(part2(tests, prog)))
