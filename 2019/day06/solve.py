#!/usr/bin/env python3

import argparse
import logging
import networkx as nx

logging.basicConfig(level=logging.DEBUG)

def part1(G):
    return sum ( ( len(nx.ancestors(G, v)) for v in G.nodes() ) )

def part2(G):
    return nx.shortest_path_length(G.to_undirected(), 'YOU', 'SAN') - 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        G = nx.DiGraph()
        for l in f:
            a, b = l.rstrip().split(')')
            G.add_edge(a, b)


    print('part1: {}'.format(part1(G)))
    print('part2: {}'.format(part2(G)))
