#!/usr/bin/env python3

from pprint import pprint
import argparse
import sys
import os
import pdb

# Get the device from previous puzzle
sys.path.append(os.path.realpath(os.path.dirname(__file__)) + '/../day_19_go_with_the_flow')
import device_opcodes

class Device_known_opcodes_monitor(device_opcodes.Device_known_opcodes):
    def __init__(self, ip):
        super(Device_known_opcodes_monitor, self).__init__(ip)
        self.states = []

    # Override to monitor the execution
    def execute_instruction(self):
        # print(self)
        instruction = self.prog[self.registers[self.ip]]
        if self.registers[self.ip] == 28:
            if self.registers in self.states:
                print('part2: self.states[-1][3])
                raise Exception('Loop detected')
            else:
                self.states.append(self.registers[:])
        self.instructions[instruction[0]](*instruction[1:])
        self.registers[self.ip] += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = []
        for l in f.readlines():
            l = l.rstrip().split()
            prog.append(tuple([l[0], *map(int, l[1:])]))

    # pdf through the program shows that the first time we have a chance of exiting, registers[0] must be 212115 to do so
    print('part1: 212115')
    d = Device_known_opcodes_monitor(prog[0][1])
    d.execute(prog[1:])
