#!/usr/bin/env python3

from pprint import pprint
import numpy as np

def gen_grid(ser):
    grid = np.zeros((300, 300))
    for x in range(300):
        for y in range(300):
            rack_id = (x+1) + 10
            power = rack_id * (y+1)
            power += ser
            power = power * rack_id
            digit = (power // 100) % 10
            digit -= 5
            grid[x,y] = digit
    return grid

def grid_check(cell, ser):
    grid = gen_grid(ser)
    return (grid[tuple ( map ( sum, zip(cell), (-1, -1)))])

def score(grid, size):
    X = 300 + 1 - size
    Y = 300 + 1 - size
    grid2 = np.zeros((X , Y))
    for x in range(X):
        for y in range(Y):
            grid2[x,y] = grid[x:x+size,y:y+size].sum()
    amax   = np.amax(grid2)
    argmax = np.unravel_index(grid2.argmax(), grid2.shape)
    return argmax[0]+1, argmax[1]+1, amax

def p1(ser):
    grid = gen_grid(ser)
    return score(grid, 3)

def p2(ser):
    grid = gen_grid(ser)
    maxs = []
    for size in range(1,300+1):
        maxs.append((*score(grid, size), size))
    return max(maxs, key=lambda x: x[2])

if __name__ == '__main__':
    assert(grid_check((3,5), 8)      == 4)
    assert(grid_check((122,79), 57)  == -5)
    assert(grid_check((217,196), 39) == 0)
    assert(grid_check((101,153), 71) == 4)
    p1 = p1(9435)
    print('P1: {},{}'.format(p1[0], p1[1]))
    p2 = p2(9435)
    print('P2: {},{},{}', p2[0], p2[1], p2[3])
