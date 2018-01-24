#!/usr/bin/env python3

from itertools import zip_longest

P1_LENGTH=272
P2_LENGTH=35651584
A = '01111010110010011'

def expand(a):
    b = ''.join([ '0' if x == '1' else '1' for x in reversed(a) ])
    return a + '0' + b

# Borrowed from: https://docs.python.org/3/library/itertools.html
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def compress(a):
    if len(a)%2 == 1:
        return a
    else:
        h = []
        for x, y in grouper(a, 2):
            if x == y:
                h.append('1')
            else:
                h.append('0')
        return compress(''.join(h))

def p(a, length):
    while len(a) < length:
        a = expand(a)
    return compress(a[0:length])

print('P1:', p(A, P1_LENGTH))
print('P2:', p(A, P2_LENGTH))
