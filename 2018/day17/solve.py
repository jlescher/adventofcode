#!/usr/bin/env python3


import argparse
import re
from collections import Counter
from pprint      import pprint
import sys


DISPLAY = False

def display_ground(ground):
    print('='*80)
    min_x = min(e[0] for e in ground)
    max_x = max(e[0] for e in ground)
    min_y = min(e[1] for e in ground)
    max_y = max(e[1] for e in ground)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            print(ground.get((x,y), '.'), end='')
        print()
    print()

def left(pos):
    return(pos[0]-1, pos[1])


def right(pos):
    return(pos[0]+1, pos[1])


def down(pos):
    return (pos[0], pos[1]+1)


def inbound(pos, dims):
    _inbound = pos[1] <= dims[1]
    if DISPLAY:
        if not _inbound:
            print(pos, 'out of bound')
    return _inbound


def explore(pos, dims, ground):
    if DISPLAY:
        display_ground(ground)
        print('exploring:', pos)

    if not inbound(pos,dims): 
        return True # We can stream down
    
    square = ground.get(pos, '.')
    if square == '#' or square == '~':
        return False

    if square == '|':
        return True

    if square != '+':
        ground[pos] = '|'

    if explore(down(pos), dims, ground):
        return True

    stream_left = explore_left(left(pos), dims, ground)
    stream_right = explore_right(right(pos), dims, ground)
    if not stream_left and not stream_right:
        # Fill on the left
        cur_pos = left(pos)
        while ground.get(cur_pos, '.') not in ('#', '~'):
            ground[cur_pos] = '~'
            cur_pos = left(cur_pos)
        # Fill on the right
        cur_pos = pos
        while ground.get(cur_pos, '.') not in ('#', '~'):
            ground[cur_pos] = '~'
            cur_pos = right(cur_pos)
    return stream_left or stream_right


def explore_left(pos, dims, ground):
    if DISPLAY:
        display_ground(ground)
        print('left exploring:', pos)

    if not inbound(pos, dims): 
        return True # We can stream down
    
    square = ground.get(pos, '.')
    if square == '#' or square == '~':
        return False

    if square == '|':
        return True

    ground[pos] = '|'

    if explore(down(pos), dims, ground):
        return True

    return explore_left(left(pos), dims, ground)


def explore_right(pos, dims, ground):
    if DISPLAY:
        display_ground(ground)
        print('right exploring:', pos)
        
    if not inbound(pos, dims): 
        return True # We can stream down
    
    square = ground.get(pos, '.')
    if square == '#' or square == '~':
        return False

    if square == '|':
        return True

    ground[pos] = '|'

    if explore(down(pos), dims, ground):
        return True

    return explore_right(right(pos), dims, ground)


def run(ground):
    dims = (min([pos[1] for pos, square in ground.items() if square == '#']), max([pos[1] for pos, square in ground.items() if square == '#']))
    display_ground(ground)
    explore((500, 0), dims, ground)
    display_ground(ground)

    # Remove the first few lines
    ground = { k:v for k,v in ground.items() if inbound(k, dims) }
    return Counter(ground.values())['|'], Counter(ground.values())['~'] 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    ground = {}
    with open(args.input) as f:
        regexp = re.compile(r'\d+')
        for l in f.readlines():
            # Parse the input
            nums = tuple(map(int, regexp.findall(l)))
            if l[0] == 'x':
                for y in range(nums[1], nums[2]+1):
                    ground[(nums[0],y)] = '#'
            elif l[0] == 'y':
                for x in range(nums[1], nums[2]+1):
                    ground[(x, nums[0])] = '#'
            else:
                raise Exception('Cannot parse line:', l)
        ground[(500,0)] = '+'

    sys.setrecursionlimit(10000)
    flow, still = run(ground)
    print('part1: {}'.format(still + flow))
    print('part2: {}'.format(flow))

