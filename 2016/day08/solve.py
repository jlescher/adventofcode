#!/usr/bin/env python3


import argparse

GRID_WIDTH = 50
GRID_HEIGHT = 6

def rect(s, grid):
    width, height = map(int, s[0].split('x'))
    for i in range(height):
        for j in range(width):
            grid.add((i, j))


def rotate(s, grid):
    pos, size = (0, GRID_WIDTH) if s[0] == 'row' else (1, GRID_HEIGHT)
    col_or_row = int(s[1].split('=')[1])
    rot = int(s[3])

    pixel_shift = { x for x in grid if x[pos] == col_or_row }
    grid.difference_update(pixel_shift)
    for x0, x1 in pixel_shift:
        if pos == 0:
            x1 = (x1 + rot) % size
        else:
            x0 = (x0 + rot) % size
        grid.add((x0, x1))


op = {
        'rect': rect,
        'rotate': rotate
        }

def print_screen(grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if (i, j) in grid:
                print('#', end='')
            else:
                print(' ', end='')
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        instructions = [ x.rstrip().split() for x in f ]

    grid = set()
    for ins in instructions:
        op[ins[0]](ins[1:], grid)
    print('P1:', len(grid))
    print('P2:')
    print_screen(grid)
