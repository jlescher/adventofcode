#!/usr/bin/env python3

import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

def get_required_fuel(mass):
    return max(0, mass // 3 - 2)

def get_all_required_fuel(mass):
    req_fuel = get_required_fuel(mass)
    tot_fuel = req_fuel
    while req_fuel > 0:
        req_fuel = get_required_fuel(req_fuel)
        tot_fuel += req_fuel
    return tot_fuel

def part1(modules):
    return sum(map(get_required_fuel, modules))

def part2(modules):
    return sum(map(get_all_required_fuel, modules))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        modules = [ int(l.rstrip()) for l in f ]

    print('part1: {}'.format(part1(modules)))
    print('part2: {}'.format(part2(modules)))
