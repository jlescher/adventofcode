#!/usr/bin/env python3


import argparse


def test_triangle(x, y, z):
    '''
    x, y, z are expected to be sorted
    '''
    return z < x + y


def possible_triangles(triangle_list):
    possible_triangles = 0
    sorted_triangles = [ sorted(x) for x in triangle_list ]
    for t in sorted_triangles:
        if test_triangle(*t):
            possible_triangles += 1
    return possible_triangles


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open('input') as f:
        l = f.readlines()
        triangles = [ tuple(map(int, x.rstrip().split())) for x in l ]

    # zip by group of three
    group3_triangles = []
    for i in range(0, len(triangles), 3):
        group3_triangles.extend(zip(*triangles[i:i+3]))

    print('P1:', possible_triangles(triangles))
    print('P2:', possible_triangles(group3_triangles))
