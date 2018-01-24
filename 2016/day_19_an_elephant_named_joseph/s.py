#!/usr/bin/env python3

from collections import deque

INPUT = 3018458

def p1(num):
    i = 0
    while 2**(i+1) <= num:
        i += 1
    a = num - 2**i
    b = 2**(i+1) - num
    if a < b:
        p1 = 1 + 2*a
    else:
        p1 = 2**(i+1) - 2*b + 1
    return p1

print('P1:', p1(INPUT))

