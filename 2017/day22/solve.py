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
    node_status = grid.get(pos, '.')
    if node_status == '.':
        direction = (direction - 1) % 4
        grid[pos] = 'W'
    elif node_status == 'W':
        grid[pos] = '#'
        cnt += 1
    elif node_status == '#':
        direction = (direction + 1) % 4
        grid[pos] = 'F'
    elif node_status == 'F':
        direction = (direction + 2) % 4
        grid[pos] = '.'
    else:
        raise(Exception)
    # Get the new position
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


def display(grid, pos):
    xmin = min(grid.keys(), key = lambda x: x[0])[0]
    xmax = max(grid.keys(), key = lambda x: x[0])[0]
    ymin = min(grid.keys(), key = lambda x: x[1])[1]
    ymax = max(grid.keys(), key = lambda x: x[1])[1]
    for y in range(ymax, ymin-1, -1):
        for x in range(xmin, xmax+1):
            print(grid.get((x, y), '.'), end='')
        print()
    print()
    print()


with open('input') as f:
    grid_list = [ l.rstrip('\n') for l in f ]
    grid_dict = {}

    # Set of infected nodes in an orthonormal 
    half_size = len(grid_list) // 2
    for y, l in enumerate(grid_list):
        for x, char in enumerate(l):
            grid_dict[(x-half_size, half_size-y)] = char

    cnt = 0
    pos = (0, 0)
    direction = UP
    display(grid_dict, pos)
    for _ in range(10000000):
        pos, direction, cnt = step(pos, direction, cnt, grid_dict)
    print(cnt)

