#!/usr/bin/env python3

import argparse
from collections import defaultdict
from itertools import cycle, islice
from pprint import pprint
from math import gcd, atan2

def get_ray(org, dst):
    '''
    Ray is defined by a source point and a vector
    vector can be expressed as (a, b) meaning "advance a steps on the x axis and b steps on the y axis"
    If PGCD(a, b) = 1 then the ray is uniquely defined
    '''
    a = dst[0] - org[0]
    b = dst[1] - org[1]
    pgcd = gcd(a, b)
    return (a//pgcd, b//pgcd), pgcd

def get_ray_map(asteroids):
    '''
    Represent the map in the following data struct:
    { asteroid: vector : [ lenght ] }
    where:
        - asteroid is the coordinates of the asteroid
        - vector is the direction of the ray
        - length is the position of the another asteroid along the vector
    '''
    ray_map = defaultdict(lambda: defaultdict(list))
    for org in asteroids:
        for dst in asteroids:
            if org != dst:
                vector, distance = get_ray(org, dst)
                ray_map[org][vector].append(distance)
    return ray_map

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))

def get_coord(base, vec, dist):
    return base[0] + vec[0]*dist, base[1] + vec[1]*dist

def part2(ray_map):
    base = max(ray_map, key=lambda x: len(ray_map[x]))

    # For each vector, sort the distances
    base_rays = { vec: sorted(dist) for vec, dist in ray_map[base].items() }

    # Rebuid the coordinates
    base_rays = { vec: list(map(lambda x: get_coord(base, vec, x), dist)) for vec, dist in base_rays.items() }

    # Sorted the vectors by atan2
    base_rays = [ coords for vec, coords in sorted(base_rays.items(), key = lambda x: atan2(x[0][0], x[0][1]), reverse=True) ]

    # Round-robin trickery
    coord = next(islice(roundrobin(*base_rays), 200-1, 200))
    return coord[0]*100 + coord[1]


def part1(ray_map):
    ray_map = [ len(v) for v in ray_map.values() ]
    return max(ray_map)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        asteroids = set()
        for y, line in enumerate(f):
            for x, char in enumerate(line):
                if char == '#':
                    asteroids.add( (i, j) )

        asteroids = [ list(l.rstrip()) for l in f.readlines() ]
            
    # Get the list of asteroids coordinates
    ray_map = get_ray_map(asteroids)

    print('part1: {}'.format(part1(ray_map)))
    print('part2: {}'.format(part2(ray_map)))
