#!/usr/bin/env python3

import argparse
import re
from collections import deque
from pprint import pprint


def draw_nodes(nodes):
    x = max(map(lambda x: x[0], nodes.keys()))
    y = max(map(lambda x: x[1], nodes.keys()))
    for n in range(y+1):
        for m in range(x+1):
            if n == 0 and m == x:
                print('G', end='')
            else:
                print(nodes[m,n], end='')
        print()


def count_viables(nodes):
    cnt = 0
    for x in nodes.values():
        for y in nodes.values():
            if x.is_viable(y):
                cnt += 1
    return cnt


def get_empty_pos(nodes):
    for pos, v in nodes.items():
        if v == '_':
            return pos
    raise(Exception())

def min_steps(nodes):
    '''
    A general solution to this problem seems hard (NP complete)A general
    solution to this problem seems hard (NP complete).
    Lets modelize the problem as suggested in the example.

    We notice that there is a single empty node.
    '''
    max_x = max(map(lambda x: x[0], nodes.keys()))
    max_y = max(map(lambda x: x[1], nodes.keys()))

    # Modelize the nodes
    # Check that there is a single empty node
    cnt_empty = 0
    for k, val in nodes.items():
        if val.used == 0:
            nodes[k] =  '_'
            cnt_empty += 1
            empty_pos = k
        elif val.used > 400:
            nodes[k] =  '#'
        else:
            nodes[k] = '.'
    assert(cnt_empty == 1)

    # Bring the 'hole' to the left of init_pos in a few moves as possible
    init_pos= (max(map(lambda x: x[0], nodes.keys())), 0)
    bfs = deque([(nodes, 0)])
    visited_pos = { get_empty_pos(nodes) }
    while len(bfs) > 0:
        nodes, step = bfs.pop()
        empty_pos = get_empty_pos(nodes)
        if empty_pos == (init_pos[0] - 1, init_pos[1]):
            break
        ex, ey = empty_pos
        for new_pos in [ (ex - 1, ey), (ex + 1, ey), (ex, ey - 1), (ex, ey + 1) ]:
            # if new_pos is viable AND new_pos never visited
            if nodes.get(new_pos, '#') == '.' and new_pos not in visited_pos:
                new_nodes = nodes.copy()
                # Move the hole to new_pos
                new_nodes[empty_pos] = '.'
                new_nodes[new_pos] = '_'
                bfs.appendleft((new_nodes, step+1))
                visited_pos.add(new_pos)
    # Verify that there are no walls on the first two lines
    for x in range(max_x+1):
        assert(nodes[(x, 0)] != '#')
        assert(nodes[(x, 1)] != '#')

    return (init_pos[0]-1)*5 + 1 + step


class Node:
    regex = re.compile(r'\D+x(?P<x>\d+)-y(?P<y>\d+)\W+(?P<size>\d+)T\W+(?P<used>\d+)T.*')

    def __init__(self, s):
        m = Node.regex.match(s)
        self.pos = (int(m.group('x')), int(m.group('y')))
        self.used = int(m.group('used'))
        self.size = int(m.group('size'))

    def available(self):
        return self.size - self.used

    def is_viable(self, other):
        return (
                self.used != 0
                and self is not other
                and self.used < other.available()
                )

    def __str__(self): 
        return '{:>4}/{:<4} '.format(self.used, self.size)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    nodes = {}
    with open(args.input) as f:
        it = iter(f)
        next(f)
        next(f)
        for l in it:
            node = Node(l)
            nodes[node.pos] = node
    print('P1:', count_viables(nodes))
    print('P2:', min_steps(nodes))

