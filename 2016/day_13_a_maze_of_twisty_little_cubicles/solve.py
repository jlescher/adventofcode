#!/usr/bin/env python3

from collections import deque

# The layout coordinates (x, y) are labelled as follow
#
#     + --> x
#     |
#     v
#     y
#


FAVORITE_NUMBER = 1362
TARGET = (31, 39)


bfs = deque([])
# Dictionnary:
# - indexed by coordinates
# Containing the status of a square and the number of steps to reach it
# dict( (0, 0): [ '.', 32 ] )
layout = {}

def get_square(x, y):
    '''
    Returns:
    -> '.' if the square is an open space
    -> '#' if the square is a wall
    '''
    num = x*x + 3*x + 2*x*y + y + y*y + FAVORITE_NUMBER
    ones = bin(num).count('1')
    return '.' if ones%2 == 0 else '#'

def explore(x, y):
    for pos in [ (x-1, y), (x+1, y), (x, y-1), (x, y+1) ]:
        if pos[0] >= 0 and pos[1] >= 0:
            if not pos in layout:
                # Add the position to the layout
                square = [ get_square(*pos), layout[(x, y)][1] + 1 ]
                layout[pos] = square
                # Add to bfs if it is not a wall
                if square[0] == '.':
                    bfs.appendleft(pos)

def draw_layout(layout):
    for y in range(30):
        for x in range(30):
            square = layout.get((x, y), ['#', 0])
            if square[0] == '#':
                string = ' #  '
            else:
                string = '{:2d}  '.format(square[1])
            print(string, end='')
        print('')

def P1():
    pos = (1, 1)
    layout[pos] = ['.', 0 ]
    bfs.appendleft(pos)
    found = False # (whoop'am Dikjstra style)
    while not found and len(bfs) > 0:
        pos = bfs.pop()
        if pos != TARGET:
            explore(*pos)
        else:
            found = True
    return layout[pos][1]

def P2():
    pos = (1, 1)
    layout[pos] = ['.', 0 ]
    bfs.appendleft(pos)
    while True:
        pos = bfs.pop()
        if layout[pos][1] == 50:
            break
        explore(*pos)
    cnt = 0
    for it, q in layout.values():
        assert(0 <= q <= 50)
        if it == '.':
            cnt += 1
    return cnt

print('P1:', P1())
# Ugly but we don't really care
bfs.clear()
layout.clear()
print('P2:', P2())
