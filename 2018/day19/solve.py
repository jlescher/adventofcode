#!/usr/bin/env python3

import argparse
import sys
import os
import pdb
from pprint import pprint
from math   import ceil, sqrt

# Get the device from previous puzzle
sys.path.append(os.path.realpath(os.path.dirname(__file__)) + '/../day_16_chronal_classification')
import device

class Device_known_opcodes(device.Device):
    def __init__(self, ip):
        super(Device_known_opcodes, self).__init__(6)
        self.ip = ip
        self.instructions = { i.__name__: i for i in self.instructions }

    def execute_instruction(self):
        # print(self)
        instruction = self.prog[self.registers[self.ip]]
        self.instructions[instruction[0]](*instruction[1:])
        self.registers[self.ip] += 1

    def execute(self, prog):
        self.prog = prog
        #pdb.set_trace()
        while True:
            try:
                self.execute_instruction()
            except IndexError:
                print('instruction pointer points out of program, exiting..')
                break

    def __str__(self):
        s = 'registers = {}\n'.format(self.registers)
        # Put the arrow in the proper location
        arrow = [ '   ' for line in self.prog ]
        nums = [ i for i in range(len(self.prog)) ]
        arrow[self.registers[self.ip]] = '-> '
        arrow_vec = map(lambda x: x[0] + ' ' + str(x[1]) + ': ' + x[2][0] + ' ' + str(x[2][1]) + ' ' + str(x[2][2]) + ' ' + str(x[2][3]), zip(arrow, nums, self.prog))
        s += '\n'.join(arrow_vec)
        return s
        


def part1(ip, prog):
    d = Device_known_opcodes(ip)
    d.execute(prog)
    return d.registers[0]


def part2(ip, prog):
    ## Takes too long -> should reverse engineer the program !
    #d = Device_known_opcodes(ip)
    #d.registers[0] = 1 # Background process
    #d.execute(prog)
    NUM = 10551315
    cnt = 0
    for i in range(1, NUM+1):
        if NUM%i == 0:
            cnt += i
    return cnt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = []
        for l in f.readlines():
            l = l.rstrip().split()
            ins = l[0]
            args = list(map(int, l[1:]))
            line = [ ins ]
            line.extend(args)
            prog.append(line)
            
    print('part0: {}'.format(part1(prog[0][1], prog[1:])))
    print('part2: {}'.format(part2(prog[0][1], prog[1:])))
