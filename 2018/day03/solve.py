#!/usr/bin/env python3

import numpy as np
import re
from pprint import pprint
import argparse

def p1(claims):
    """
    Would maintaining a dictionnary with:
    - keys = square coordinates
    - values = list of id that claim the square
    be faster?
    """
    fabric = np.zeros((1000, 1000))
    for c in claims:
        for i in range(c['top'], c['top'] + c['height']):
            for j in range(c['left'], c['left'] + c['width']):
                fabric[i, j] += 1
    # Is there a faster way?
    return (fabric > 1).sum()

def p2(claims):
    overlap = set()
    fabric = np.zeros((1000, 1000))
    for c in claims:
        for i in range(c['top'], c['top'] + c['height']):
            for j in range(c['left'], c['left'] + c['width']):
                if fabric[i, j] == 0:
                    # Mark the box as being "used" by id.
                    fabric[i, j] += c['id']
                else:
                    # Collision: both claims overlap.
                    overlap.add(fabric[i, j])
                    overlap.add(c['id'])
    # Remove the ids that overlap.
    ids = set(map(lambda x: x['id'], claims))
    return ids.difference(overlap).pop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    claims = []
    r = re.compile('#(?P<id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)')
    with open(args.input) as f:
        for l in f.readlines():
            m = r.match(l)
            d = {
                    'id':     int(m.group('id')),
                    'left':   int(m.group('left')),
                    'top':    int(m.group('top')),
                    'width':  int(m.group('width')),
                    'height': int(m.group('height')),
                    }
            claims.append(d)
    print('P1: ', p1(claims))
    print('P2: ', p2(claims))
