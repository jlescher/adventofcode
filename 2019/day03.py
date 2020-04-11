#!/usr/bin/env python3

import argparse
import logging
import pdb

logging.basicConfig(level=logging.WARNING)

move = {
        'R': lambda x, y: (x+1, y),
        'L': lambda x, y: (x-1, y),
        'U': lambda x, y: (x  , y+1),
        'D': lambda x, y: (x  , y-1),
        }

def get_path(wire):
    x, y = 0, 0
    path = list()
    for direction, num in wire:
        for _ in range(num):
            x, y = move[direction](x, y)
            path.append((x, y))
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        wires = []
        for l in f:
            l = l.rstrip().split(',')
            l = [ x[0], int(x[1:]) for x in l ]
            wires.append(l)

    wire1 = list(get_path(wires[0]))
    wire2 = list(get_path(wires[1]))
    intersection = set(wire1).intersection(set(wire2))

    dist = [ sum( map( abs, x)) for x in intersection ]
    time = [ wire1.index(x) + wire2.index(x) for x in intersection ]

    print('part1: {}'.format(min(dist)))
    print('part2: {}'.format(min(time)+2))
        

        
