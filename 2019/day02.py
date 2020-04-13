#!/usr/bin/env python3

import argparse
import logging
from lib.intcode import VM

def run_noun_verb(noun, verb, exe):
    exe = exe[:]
    exe[1] = noun
    exe[2] = verb
    vm = VM(exe)
    while True:
        try:
            _ = next(vm.run(1))
        except StopIteration:
            break
    return vm.memory[0]

def part1(exe):
    return run_noun_verb(12, 2, exe)

def part2(exe):
    for noun in range(100):
        for verb in range(100):
            logging.info('noun:{} verb:{}'.format(noun, verb))
            if run_noun_verb(noun, verb, exe) == 19690720:
                return 100*noun + verb

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        exe = list(map(int, f.readline().split(',')))

    print('part1: {}'.format(part1(exe)))
    print('part2: {}'.format(part2(exe)))
