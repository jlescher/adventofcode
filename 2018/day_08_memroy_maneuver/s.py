#!/usr/bin/env python3

from collections import defaultdict
from pprint import pprint
import copy
import argparse
import re

def dfs1_node(index, flat, cnt):
    num_child = flat[index]
    num_meta =  flat[index+1]
    index += 2
    for _ in range(num_child):
        index, cnt = dfs1_node(index, flat, cnt)
    for i in range(num_meta):
        cnt += flat[index+i]
    index += num_meta
    return index, cnt

def dfs2_node(index, flat, cnt):
    num_child = flat[index]
    num_meta =  flat[index+1]
    index += 2
    vals = {}
    for i in range(num_child):
        index, icnt = dfs2_node(index, flat, 0)
        vals[i+1] = icnt
    # Value
    cnt = 0
    if len(vals) is 0:
        for i in range(num_meta):
            cnt += flat[index+i]
    else:
        for i in range(num_meta):
            try:
                cnt += vals[flat[index+i]]
            except:
                pass
    index += num_meta
    return index, cnt

def p1(flat):
    return dfs1_node(0, flat, 0)[1]

def p2(flat):
    return dfs2_node(0, flat, 0)[1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        flat = list(map(int, f.readlines()[0].rstrip().split(' ')))

    print('P1: ', p1(flat))
    print('P2: ', p2(flat))
