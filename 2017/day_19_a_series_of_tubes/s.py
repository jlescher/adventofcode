#!/usr/bin/env python3

import string
from pprint import pprint as print

# up    = 0
# right = 1
# down  = 2
# left  = 3

with open('input') as f:
    matrix = []
    letters = []
    for l in f:
        matrix += [l.rstrip('\n')]
    row = 0
    col = matrix[0].index('|')
    direction = 2
    step = -2
    while True:
        step += 1
        # Find the next '+'
        while matrix[row][col] != '+':
            step += 1
            a = matrix[row][col]
            if matrix[row][col] == ' ':
                print(''.join(letters))
                print(step)
                quit()
            if matrix[row][col] in string.ascii_uppercase:
                letters.append(matrix[row][col])
            if direction == 0:
                row -= 1
            elif direction == 1:
                col += 1
            elif direction == 2: 
                row += 1
            elif direction == 3:
                col -= 1
            else:
                raise(Exception)
        # Find the next direction
        if direction % 2 == 0:
            if matrix[row][col-1] != ' ':
                col -= 1
                direction = 3
            elif matrix[row][col+1] != ' ':
                col += 1
                direction = 1
            else:
                raise(Exception)
        else:
            if matrix[row-1][col] != ' ':
                row -= 1
                direction = 0
            elif matrix[row+1][col] != ' ':
                row += 1
                direction = 2
            else:
                raise(Exception)
