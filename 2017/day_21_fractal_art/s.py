#!/usr/bin/env python3

import math
from pprint import pprint as print

# Represent a matrix as a dictionnary where:
#   - keys are the coordinates of a square
#   - values are the content of a square
matrix_list = [ '.#.', '..#', '###' ]
matrix_dict = {}
for i in range(len(matrix_list)):
    for j in range(len(matrix_list[0])):
        matrix_dict[(i, j)] = matrix_list[i][j]

patterns = {}

def add_pattern(patterns, line):
    # Sad but true
    pattern, output = line.rstrip().split(' => ')
    patterns[pattern] = output
    for _ in range(3):
        pattern = rotate_clockwise(pattern)
        patterns[pattern] = output
    if len(pattern) == 11:
        pattern = flip(pattern)
        patterns[pattern] = output
        for _ in range(3):
            pattern = rotate_clockwise(pattern)
            patterns[pattern] = output

def rotate_clockwise(p):
    """
    Rotate clockwise:
    01/34 -> 30/41
    012/456/89a -> 840/951/a62
    """
    if len(p) == 5:
        return p[3] + p[0] + p[2] + p[4] + p[1]
    elif len(p) == 11:
        return p[8] + p[4] + p[0] + p[3] + p[9] + p[5] + p[1] + p[7] + p[10] + p[6] + p[2]
    else:
        raise(Exception)

def flip(p):
    """
    Flip horizontally
    012/456/89a -> 89a/456/012
    """
    if len(p) == 11:
        return p[8] + p[9] + p[10] + p[3] + p[4] + p[5] + p[6] + p[7] + p[0] + p[1] + p[2]
    else:
        raise(Exception)


def get_pattern(matrix_dict, i, j, size):
    """
    Return the pattern extracted from the matrix as listed in the input
    """
    pattern = ''
    for m in range(i, i+size):
        for n in range(j, j+size):
            pattern += matrix_dict[(m, n)]
        pattern += '/'
    return pattern[0:-1]


def get_pieces(matrix_dict, size):
    pieces = {}
    sqrt = int(math.sqrt(len(matrix_dict)))
    for i in range(0, sqrt, size):
        for j in range(0, sqrt, size):
            pieces[(i//size, j//size)] = get_pattern(matrix_dict, i, j, size)
    return pieces


def assemble_matrix(pieces):
    """
    Reverse operation of split_matrix
    """
    matrix_dict = {}
    piece_size = len(pieces[(0, 0)].split('/')[0])
    for key, val in pieces.items():
        for i in range(piece_size):
            for j in range(piece_size):
                matrix_dict[(key[0]*piece_size +i, key[1]*piece_size + j)] = val.replace('/', '')[piece_size*i + j]
    return matrix_dict


def split_matrix(matrix_dict):
    """
    Return a dictionnary where:
        - keys are coordinates of the split matrix in 'size' unit
        - values is the string representation of a pattern
    """
    if len(matrix_dict) % 2 == 0:
        pieces = get_pieces(matrix_dict, 2)
    else:
        pieces = get_pieces(matrix_dict, 3)
    return pieces


def convert(pieces, patterns):
    for k, v in pieces.items():
        pieces[k] = patterns[v]
    return pieces

with open('input') as f:
    for l in f:
        add_pattern(patterns, l)
    for i in range(18):
        matrix_dict = assemble_matrix(convert(split_matrix(matrix_dict), patterns))
    cnt = 0
    for v in matrix_dict.values():
        if v == '#':
            cnt += 1
    print(cnt)

