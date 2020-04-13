#!/usr/bin/env python3

import argparse
from lib.intcode import VM


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        exe = list(map(int, f.readline().split(',')))

    vm = VM(exe).run(1)
    while True:
        try:
            out = next(vm)
        except StopIteration:
            break

    print('part1: {}'.format(out))

    vm = VM(exe).run(2)
    while True:
        try:
            out = next(vm)
        except StopIteration:
            break

    print('part2: {}'.format(out))
