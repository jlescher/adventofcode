#!/usr/bin/env python3

import argparse
import logging
import networkx as nx

logging.basicConfig(level=logging.DEBUG)

def part1(G):
    return sum ( [ len(nx.ancestors(G, v)) for v in G.nodes() ] )

def part2(G):
    common = nx.lowest_common_ancestor(G, 'YOU', 'SAN')
    return len(nx.shortest_path(G, common, 'YOU')) + len(nx.shortest_path(G, common, 'SAN')) - 4

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        G = nx.DiGraph()
        for l in f:
            G.add_edge(*(l.rstrip().split(')')))


    print('part1: {}'.format(part1(G)))
    print('part2: {}'.format(part2(G)))
