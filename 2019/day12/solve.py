#!/usr/bin/env python3

from copy      import deepcopy
from functools import reduce
from itertools import permutations
from math      import gcd
import argparse
import logging
import re

def dx(x, y):
    if x < y:
        return 1
    if x == y:
        return 0
    return -1

def lcm(a, b):
    return a * b // gcd (a, b)
    
class Moon:
    def __init__(self, pos):
        self.pos = pos
        self.vel = tuple( (0 for _ in self.pos) )

    def apply_gravity(self, moon):
        self.vel = tuple( (vel + dx(pos0,pos1) for vel, pos0, pos1 in zip(self.vel, self.pos, moon.pos)) )

    def move(self):
        self.pos = tuple( ( pos+vel for pos, vel in zip(self.pos, self.vel) ) )
            
    def get_energy(self):
        return sum(map(abs, self.pos)) * sum(map(abs, self.vel))

    def __hash__(self):
        return hash((self.pos, self.vel))

    def __str__(self):
        return 'pos: {} vel: {}'.format(self.pos, self.vel)

class Universe:
    def __init__(self, moons):
        self.moon_axis = [ [ Moon(((x),)) for x in y ] for y in (zip( *[ m.pos for m in moons ] )) ]

    def repeat_len_axis(self, moons):
        states = set()
        states.add(tuple(moons))
        while True:
            step(moons)
            state = tuple(moons)
            if state in states:
                return len(states)
            else:
                states.add(state)

    def repeat_len(self):
        repeat = [ self.repeat_len_axis(m) for m in self.moon_axis ]
        return reduce(lcm, repeat)
        
def step(moons):
    for m, n in permutations(moons, 2):
        m.apply_gravity(n)
    for m in moons:
        m.move()

def part2(moons):
    # We notice that each components x, y and z axis are independant
    # So we can run the loop detection on each axis and return the ppcm of that
    universe = Universe(moons)
    return universe.repeat_len()

def part1(moons):
    moons = deepcopy(moons)
    for steps in range(1000):
        step(moons)
        logging.debug('After {} steps:'.format(steps))
        for m in moons:
            logging.debug(m)
    return sum(map(Moon.get_energy, moons))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        moons = []
        for l in f:
            pos = tuple(map(int, re.findall('-?\d+', l)))
            moons.append(Moon(pos))

    print('part1: {}'.format(part1(moons)))
    print('part2: {}'.format(part2(moons)))
