#!/usr/bin/env python3

from math import sqrt

PUZZLE_INPUT = 325489

def spiral_coordinates():
    '''
    Generator yielding the successive coordinates of the spiral
    '''
    x, y = 0, 0
    while True:
        yield x, y
        if x > 0 and y < x and y > -x:
            y += 1
        elif y > 0 and x > -y and x <= y:
            x -= 1
        elif x < 0 and y > x and y <= -x:
            y -= 1
        elif y <= 0 and x <= -y:
            x += 1
        else:
            print('Should not land here, x:{}, y:{}'.format(x, y))
            raise(Exception)

# P1
for i, coord in enumerate(spiral_coordinates(), 1):
    if i == PUZZLE_INPUT:
        print('P1:', sum(map(abs, coord)))
        break

def get_neighbor_sum(coord, spiral):
    cnt = 0
    for x in range(coord[0] - 1, coord[0] + 2):
        for y in range(coord[1] - 1, coord[1] + 2):
            cnt += spiral.get((x, y), 0)
    return cnt

# P2
spiral = {(0, 0): 1}
for coord in spiral_coordinates():
    val = get_neighbor_sum(coord, spiral)
    spiral[coord] = val
    if val > PUZZLE_INPUT:
        print('P2:', val)
        break

