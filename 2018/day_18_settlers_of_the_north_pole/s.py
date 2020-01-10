#!/usr/bin/env python3


import argparse
from pprint import pprint
from copy   import deepcopy


def display(area):
    print('='*80)
    for line in area:
        for char in line:
            print(char, end='')
        print()
    print()

def get_adjacent(x, y, area):
    adjacent = []
    for i in range(x-1, x+1 +1):
        for j in range(y-1, y+1 +1):
            if (x,y) != (i,j) and i >=0 and j >= 0:
                try:
                    adjacent.append(area[i][j])
                except:
                    pass
    return adjacent.count('.'), adjacent.count('|'), adjacent.count('#')



def tick(area):
    area_new  = [ list(l) for l in area ]
    for x, l in enumerate(area):
        for y, char in enumerate(l):
            opened, wooded, lumberyard = get_adjacent(x, y, area)
            if char == '.':
                if wooded >= 3:
                    area_new[x][y] = '|'
            elif char == '|':
                if lumberyard >= 3:
                    area_new[x][y] = '#'
            elif char == '#':
                if not (lumberyard >= 1 and wooded >= 1):
                    area_new[x][y] = '.'
    return tuple(tuple(l) for l in area_new)

def part1(area):
    # Do not touch the input
    area_new = deepcopy(area)
    for minute in range(10):
        area_new = tick(area_new)
    cnt_wooded     = sum( [ x.count('|') for x in area_new ] )
    cnt_lumberyard = sum( [ x.count('#') for x in area_new ] )
    return cnt_wooded * cnt_lumberyard

def part2(area):
    # Do not touch the input
    area_new = deepcopy(area)

    states = {} # hashmap to detect repeating positions
    states[area_new] = 0

    cnt = 0
    while True:
        area_new = tick(area_new)
        cnt += 1
        try:
            cnt_repeat = states[area_new]
            break
        except KeyError:
            states[area_new] = cnt

    cnt_ref = cnt_repeat + ( (1000000000 - cnt_repeat) % (cnt - cnt_repeat))
    for k, v in states.items():
        if v == cnt_ref:
            area_new = k
    cnt_wooded     = sum( [ x.count('|') for x in area_new ] )
    cnt_lumberyard = sum( [ x.count('#') for x in area_new ] )
    return cnt_wooded * cnt_lumberyard

        
        
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        area = tuple( tuple(l.rstrip()) for l in f.readlines() )
    print('part1: {}'.format(part1(area)))
    print('part2: {}'.format(part2(area)))

