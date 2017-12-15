#!/usr/bin/env python3

#from pprint import pprint as print
import sys
sys.path.insert(0, '../j10_knot_hash/')
from s import knot_hash

KEY_STRING = 'hwlqcszp'

def explore(grid, i, j):
    if grid[i][j] == 0:
        return
    else:
        grid[i][j] = 0 # Mark as visited, won't be used again
        if i > 0:
            explore(grid, i-1, j)
        if i < len(grid) -1:
            explore(grid, i+1, j)
        if j > 0:
            explore(grid, i, j-1)
        if j < len(grid[0]) - 1:
            explore(grid, i, j+1)

grid = []
for i in range(128):
    kh = knot_hash('{}-{}'.format(KEY_STRING, i))
    v = []
    for i, n in enumerate(kh):
        v = v + list(map(int, '{:08b}'.format(n)))
    grid.append(v)

cc = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] != 0:
            cc += 1
            explore(grid, i, j)
print(cc)
