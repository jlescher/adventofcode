#!/usr/bin/env python3

import argparse
import re
from pprint import pprint

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

    def execute(self, instruction):
        opcode, A, B, C = instruction.split(' ')

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

def part2(tests):
    d = Device()
    opcodes = [ dict() for instruction in d.instructions ]
    pprint(opcodes)


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
    
    print('part1: {}'.format(part1(tests)))
