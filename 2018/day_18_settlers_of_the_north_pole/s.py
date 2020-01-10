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



def tick(area)
def part1(area):
    # Do not touch the input
    area_init = deepcopy(area)
    area_new  = deepcopy(area)
    #display(area_init)
    for minute in range(10):
        for x, l in enumerate(area_init):
            for y, char in enumerate(l):
                opened, wooded, lumberyard = get_adjacent(x, y, area_init)
                if char == '.':
                    if wooded >= 3:
                        area_new[x][y] = '|'
                elif char == '|':
                    if lumberyard >= 3:
                        area_new[x][y] = '#'
                elif char == '#':
                    if not (lumberyard >= 1 and wooded >= 1):
                        area_new[x][y] = '.'
        area_init = deepcopy(area_new)
        #display(area_init)
    cnt_wooded     = sum( [ x.count('|') for x in area_init ] )
    cnt_lumberyard = sum( [ x.count('#') for x in area_init ] )
    return cnt_wooded * cnt_lumberyard
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        area = [ list(l.rstrip()) for l in f.readlines() ]
    print('part1: {}'.format(part1(area)))

