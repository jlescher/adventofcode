#!/usr/bin/env python3

from collections import defaultdict
from pprint import pprint
import copy
import argparse
import re

def draw(pos):
    pos = { x[0] for x in pos }
    top_left = (min(pos, key=lambda x: x[0])[0], min(pos, key=lambda x: x[1])[1])
    bot_right = (max(pos, key=lambda x: x[0])[0], max(pos, key=lambda x: x[1])[1])

    for y in range(top_left[1], bot_right[1] + 1):
        for x in range(top_left[0], bot_right[0] + 1):
            if (x, y) in pos:
                print('#', end='')
            else:
                print('.', end='')
        print()

def move(pos):
    return list( map( lambda x: ( tuple ( map ( sum, zip(x[0], x[1]))), x[1] ), pos) )

def p(pos):
    # Loop until all points are within 50 height
    t = 0
    while True:
        miny = min(pos, key=lambda x: x[0][1])[0][1]
        maxy = max(pos, key=lambda x: x[0][1])[0][1]
        if maxy - miny < 15:
            draw(pos)
            break
        else:
            t += 1
            pos = move(pos)
    return t

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        lines = f.readlines()

    # Extract part1 input
    tests = []
    i = 0
    while 'Before' in in lines[i]:
        # Create the unit test

