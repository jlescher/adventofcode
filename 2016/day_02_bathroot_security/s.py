#!/usr/bin/env python3

import argparse

def get_keypad1():
    keypad = {}
    for i in range(3):
        for j in range(3):
            keypad[(i, j)] = str(3*i+j + 1)
    return keypad


def get_keypad2():
    keypad = {
            (0, 2): '1',
            (1, 1): '2',
            (1, 2): '3',
            (1, 3): '4',
            (2, 0): '5',
            (2, 1): '6',
            (2, 2): '7',
            (2, 3): '8',
            (2, 4): '9',
            (3, 1): 'A',
            (3, 2): 'B',
            (3, 3): 'C',
            (4, 2): 'D',
            }
    return keypad


def dial(keypad, pos, instructions, directions):
    code = ''
    for ins in instructions:
        for d in ins:
            new_pos = directions[d](*pos)
            if new_pos in keypad.keys():
                pos = new_pos
        code += keypad[pos]
    return code


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    # Read the instructions
    with open(args.input) as f:
        instructions = f.readlines()
        instructions = [ x.rstrip() for x in instructions ]

    directions = {
            'U' : lambda x, y: (x-1, y),
            'D' : lambda x, y: (x+1, y),
            'L' : lambda x, y: (x  , y-1),
            'R' : lambda x, y: (x  , y+1)
            }

    print('P1:', dial(get_keypad1(), (2, 2), instructions, directions))
    print('P2:', dial(get_keypad2(), (1, 1), instructions, directions))
