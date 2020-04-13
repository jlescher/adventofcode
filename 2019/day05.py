#!/usr/bin/env python3

import argparse
from lib.intcode import VM

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
            exe = list(map(int, f.readline().split(',')))

    vm = VM(exe)
    while True:
        try:
            out = next(vm.run(1))
        except StopIteration:
            break

    print('part1: {}'.format(out))

    vm = VM(exe)
    out = vm.run(5)
    
    print('part2: {}'.format(out))
