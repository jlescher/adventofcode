#!/usr/bin/env python3

import argparse
import re

class Disk:
    def __init__(self, num, init_pos, num_pos):
        self.num = num
        self.init_pos = init_pos
        self.num_pos = num_pos

    def capsule_pass(self, t):
        return (self.num + self.init_pos + t) % self.num_pos == 0

def p(disks):
    time = 0
    while True:
        for d in disks:
            if not d.capsule_pass(time):
                break
        else:
            return time
        time += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    regex = re.compile(r'\D*(?P<num>\d*)\D*(?P<num_pos>\d*)\D*0\D*(?P<pos>\d*)\D*')
    with open(args.input) as f:
        # disk contains the position of each disk when the capsule reach it
        disks = []
        for l in f:
            m = regex.match(l)
            disks.append(Disk(int(m.group('num')), int(m.group('pos')), int(m.group('num_pos'))))

    disks.sort(key=lambda x: x.num_pos, reverse=True)
    print('P1:', p(disks))
    disks.append(Disk(len(disks)+1, 0, 11))
    disks.sort(key=lambda x: x.num_pos, reverse=True)
    print('P2:', p(disks))
