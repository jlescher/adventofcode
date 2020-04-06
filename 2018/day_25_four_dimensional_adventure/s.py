#!/usr/bin/env python3

import argparse
import operator

logging.basicConfig(level=logging.WARNING)

def connected(v1, v2):
    return sum(map(abs, map (operator.sub, v1, v2))) <= 3

def part1(vertices):
    vertices = vertices.copy()

    # Put each vertex in its own component
    components = {}
    for i, vertex in enumerate(vertices):
        components[vertex] = i

    # For each edge, union the components
    while vertices:
        cur_vertex = vertices.pop()
        for vertex in vertices:
            if connected(vertex, cur_vertex):
                # Union
                components = { k: v if v != components[vertex] else components[cur_vertex] for k, v in components.items() }

    return len(set(components.values()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        vertices = set()
        for l in f.readlines():
            vertices.add(tuple(map(int, l.rstrip().split(','))))

    print('part1: {}'.format(part1(vertices)))
