#!/usr/bin/env python3

import argparse
from collections import deque

north = lambda x, y: (x  , y+1)
east  = lambda x, y: (x+1, y  )
south = lambda x, y: (x  , y-1)
west  = lambda x, y: (x-1, y  )

def get_dist(pos):
    return sum(map(abs, pos))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    trigger_P2 = True
    positions = set()
    with open(args.input) as f:
        instructions = f.read().rstrip().split(', ')

        direction = deque([north, east, south, west])
        pos = (0, 0)
        for ins in instructions:
            if ins[0] == 'L':
                direction.rotate(1)
            else:
                direction.rotate(-1)
            for _ in range(int(ins[1:])):
                pos = direction[0](*pos)
                if trigger_P2:
                    if pos in positions:
                        saved_pos = pos
                        trigger_P2 = False
                    else:
                        positions.add(pos)
        print('P1:', get_dist(pos))
        print('P2:', get_dist(saved_pos))
