#!/usr/bin/env python3

with open('input') as f:
    keypad = [[ 1, 2, 3], [4, 5, 6], [7, 8, 9]]
    pos = [1, 1]
    for l in f:
        for c in l.strip():
            saved_pos = pos[:]
            if c == 'U':
                pos[0] -= 1
            elif c == 'L':
                pos[1] -= 1
            elif c =='D':
                pos[0] += 1
            elif c == 'R':
                pos[1] += 1
            else:
                print('We should not land here, this is an issue')
            if pos[0] < 0 or pos[0] >= len(keypad) or pos[1] < 0 or pos[1] >= len(keypad[0]):
                pos = saved_pos
        print(keypad[pos[0]][pos[1]], end='')

