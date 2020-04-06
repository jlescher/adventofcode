#!/usr/bin/env python3

from itertools import tee
from collections import deque
from pprint import pprint
import argparse

def p(state, patterns, steps):
    index = 0 # index of the first element

    for loop in range(1, steps+1):
        # Extend state
        if state[0] == '#' :
            state = '.'*2 + state
            index += 2
        elif state[1] == '#':
            state = '.' + state
            index += 1
        if state[-1] == '#':
            state = state + '.'*2
        elif state[-2] == '#':
            state = state + '.'

        state = '..' + state + '..'
        new_state = ''
        for i in range(2, len(state) - 2):
            if state[i-2:i+2+1]in patterns:
                new_state += '#'
            else:
                new_state += '.'
        state = new_state

        cnt = 0
        for i, pot in enumerate(state):
            if pot == '#':
                cnt += (i-index)
        print('loop:{} cnt:{}'.format(loop, cnt))
    return cnt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    patterns = set()
    with open(args.input) as f:
        for i, l in enumerate(f.read().splitlines()):
            if i is 0:
                state = l.split(' ')[2]
            elif i is 1:
                pass
            else:
                pat, _, plant = l.split(' ')
                if plant == '#':
                    patterns.add(pat)
    print('P1: ', p(state, patterns, 20))
    print('P1: ', p(state, patterns, 50000000000))
