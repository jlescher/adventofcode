#!/usr/bin/env python3


def test_triangle(x, y, z):
        return z < x + y

with open('input') as f:
    possible_triangles = 0
    l = list(map(lambda x: map(int, x.split()), list(f)))
    for i in range(0, len(l), 3):
        p = list(map(sorted, zip(*l[i:i+3])))
        for t in p:
            if test_triangle(*t):
                possible_triangles += 1
    print(possible_triangles)
