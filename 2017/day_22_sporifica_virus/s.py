#!/usr/bin/env python3

from pprint import pprint
from enum import Enum
from math import sqrt


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def get_middle(grid):
    '''
    Get the coordinates of the middle of the grid based on the number of squares.
    '''
    middle = (int(sqrt(len(grid))) - 1) // 2
    return middle, middle


def step(pos, direction, cnt, grid):
    # Get new direction and toggle node
    if pos in grid:
        direction = (direction + 1) % 4
        grid.remove(pos)
    else:
        direction = (direction - 1) % 4
        grid.add(pos)
        cnt += 1
    # Move forward
    if direction == UP:
        pos = pos[0] , pos[1] + 1
    elif direction == RIGHT:
        pos = pos[0] + 1, pos[1]
    elif direction == DOWN:
        pos = pos[0], pos[1] - 1
    elif direction == LEFT:
        pos = pos[0] - 1, pos[1]
    else:
        raise(Exception)
    return  pos, direction, cnt


with open('input') as f:
    grid_list = [ l.rstrip('\n') for l in f ]
    grid_list.reverse()
    grid_set = set()

    # Set of infected nodes in an orthonormal 
    ymin = - (len(grid_list)    // 2)
    xmin = - (len(grid_list[0]) // 2)
    for y, l in enumerate(grid_list, ymin):
        for x, char in enumerate(l, xmin):
            if char == '#':
                grid_set.add((x, y))

    cnt = 0
    pos = (0, 0)
    direction = UP
    for _ in range(10000):
        pos, direction, cnt = step(pos, direction, cnt, grid_set)
    print(cnt)

