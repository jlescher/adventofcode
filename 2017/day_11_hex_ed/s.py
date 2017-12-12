#!/usr/bin/env python3

# For each hex, lets consider that (i, j) represens the coordinates of its lower left corner.
# To accomodate with the shape of hexagone lets consider that:
# - going North is like doing (i, j+2)
# - going South is like doing (i, j-2)
# - going NE    is like doing (i+1, j+1)
# - going NW    is like doing (i+1, j-1)
# - going SE    is like doing (i-1, j+1)
# - going SW    is like doing (i-1, j+1)

def north(coord):
    coord[1] += 2

def south(coord):
    coord[1] -= 2

def ne(coord):
    coord[0] += 1
    coord[1] += 1

def nw(coord):
    coord[0] -= 1
    coord[1] += 1

def se(coord):
    coord[0] += 1
    coord[1] -= 1

def sw(coord):
    coord[0] -= 1
    coord[1] -= 1

direct = {
        'n': north,
        's': south,
        'ne': ne,
        'nw': nw,
        'se': se,
        'sw': sw
        }

def get_pos(coord):
    return  (abs(org[0]) +  abs(org[1])) // 2

with open('input') as f:
    org = [0, 0]
    max_step_away = 0
    directions = f.readline().rstrip().split(',')
    for d in directions:
        direct[d](org)
        max_step_away = max(max_step_away, get_pos(org))
    print('max_step_away: {}'.format(max_step_away))
    print('step_away: {}'.format(get_pos(org)))
