#!/usr/bin/env python3

from collections import Counter
from pprint import pprint
import argparse

"""
The grid is numbered as in the example:
    (column, row)
"""

def manhattan_dist(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])

def closest(p0, coordinates):
    """
    Returns:
    None is several points are equally close to p0.
    The index of the points which is the closest to p0.
    """
    dists = [ manhattan_dist(p0, c) for c in coordinates ]
    if dists.count(min(dists)) > 1: # equidistant
        return None
    else:
        return dists.index(min(dists))

    
def p1(coordinates):
    """
    If the grid looks as such:
    ..........
    .A........
    ..........
    ........C.
    ...D......
    .....E....
    .B........
    ..........
    ..........
    ........F.

    Create a rectangle with the top most, left most, right most point as such:
    ..........
    .A#######.
    .#......#.
    .#......C.
    .#.D....#.
    .#...E..#.
    .B......#.
    .#......#.
    .#......#.
    .#######F.

    Compute the distances for all the points 
    """

    top    = min(coordinates, key = lambda k: k[1])[1]
    bottom = max(coordinates, key = lambda k: k[1])[1]
    left   = min(coordinates, key = lambda k: k[0])[0]
    right  = max(coordinates, key = lambda k: k[0])[0]
    distances = {}
    infinite  = set()
    for i in range(left, right+1):
        for j in range(top, bottom+1):
            p = (i, j)
            p_close = closest(p, coordinates)
            distances[p] = p_close
            if i == left or i == right or j == top or j == bottom: # on the edge
                infinite.add(p_close)

    # Filter-out the un-eligible summits
    filtered_distances = { k:v for k,v in distances.items() if v is not None and v not in infinite }
    c = Counter(filtered_distances.values())
    return c.most_common(1)[0][1]


def p2(coordinates):
    top    = min(coordinates, key = lambda k: k[1])[1]
    bottom = max(coordinates, key = lambda k: k[1])[1]
    left   = min(coordinates, key = lambda k: k[0])[0]
    right  = max(coordinates, key = lambda k: k[0])[0]

    cnt = 0
    cum_dist = 0
    for i in range(left-15, right+15):
        for j in range(top-15, bottom+15):
            p = (i, j)
            cum_dist = 0
            for c in coordinates:
                if cum_dist > 10000:
                    break
                else:
                    cum_dist += manhattan_dist(p, c)
            if cum_dist < 10000:
                cnt += 1
    return cnt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        coordinates = [ tuple(map(int, l.rstrip().split(', '))) for l in f.readlines()]

    print('P1: ', p1(coordinates))
    print('P2: ', p2(coordinates))
