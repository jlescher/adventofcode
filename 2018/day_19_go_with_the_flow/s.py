#!/usr/bin/env python3

import argparse
import sys
import os
import pprint

# Get the device from previous puzzle
sys.path.append(os.path.realpath(os.path.dirname(__file__)) + '/../day_16_chronal_classification')
import device

class Device_known_opcodes(device.Device):
    def __init__(self, ip):
        super(Device_known_opcodes, self).__init__(6)
        self.ip = ip
        self.instructions = { i.__name__: i for i in self.instructions }

    def execute(self, prog):
        self.prog = prog
        while True:
            #print(self)
            try:
                instruction = self.prog[self.registers[self.ip]]
            except IndexError:
                print('instruction pointer points out of program, exiting..')
                break
            self.instructions[instruction[0]](*instruction[1:])
            self.registers[self.ip] += 1

    def __str__(self):
        try:
            instruction = self.prog[self.registers[self.ip]]
        except IndexError:
            instruction = 'out of range'
        return "ip={} {} {}".format(self.registers[self.ip], self.registers, instruction)


def part1(ip, prog):
    d = Device_known_opcodes(ip)
    d.execute(prog)
    return d.registers[0]


def part2(ip, prog):
    # Takes too long -> should reverse engineer the program !
    d = Device_known_opcodes(ip)
    d.registers[0] = 1 # Background process
    d.execute(prog)
    return d.registers[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = []
        for l in f.readlines():
            ins, *args = l.rstrip().split()
            prog.append(tuple([ins, *map(int, args)]))

    print('part1: {}'.format(part1(prog[0][1], prog[1:])))
    print('part2: {}'.format(part2(prog[0][1], prog[1:])))
