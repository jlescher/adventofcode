#!/usr/bin/env python3

import itertools
import collections
import argparse

def hamming(s1, s2):
    if len(s1) != len(s2):
        return -1
    cnt = 0
    for l1, l2 in zip(s1, s2):
        if l1 != l2:
            cnt += 1
    return cnt

def cnt(id):
    c = collections.Counter(id)
    return int(2 in c.values()), int(3 in c.values())

def p1(ids):
    cnts = (0, 0)
    for id in ids:
        cnts = list(map(sum, zip(cnts, cnt(id))))
    # Poor man's reduce multiplication
    return cnts[0] * cnts[1]

def p2(ids):
    for s1, s2 in itertools.combinations(ids, 2):
        # It seems that there is only one couple of strings that differ by 1 letter.
        # Take the first hit.
        if hamming(s1, s2) == 1:
            # Return the string in common
            s = ''
            for l1, l2 in zip(s1, s2):
                if l1 == l2:
                    s += l1
            return s



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        ids = [ l.rstrip() for l in f.readlines() ]
    print('P1: ', p1(ids))
    print('P2: ', p2(ids))
