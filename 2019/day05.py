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
    out = vm.run_pack(1)[-1]
    
    print('part1: {}'.format(out))

    vm.reset()
    vm.reset_memory(exe)
    out = vm.run_pack(5).pop()
    
    print('part2: {}'.format(out))
