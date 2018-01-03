#!/usr/bin/env python3

from pprint import pprint

def build_bridge(node, edges):
    bridge_weight = 0
    for edge in edges:
        if node in edge:
            edges_left = edges[:]
            edges_left.remove(edge)
            bridge_weight = max(build_bridge(sum(edge)-node, edges_left), bridge_weight)
    if bridge_weight == 0: # Leaf
        return node
    else: # At least one domino can be connected to node
        return bridge_weight + 2*node


def get_longest_then_heaviest_bridge(node, edges):
    lenght_and_weight = set()
    for edge in edges:
        if node in edge:
            edges_left = edges[:]
            edges_left.remove(edge)
            lenght_and_weight.add(get_longest_then_heaviest_bridge(sum(edge)-node, edges_left))
    if len(lenght_and_weight) == 0: # Leaf
        return 1, node
    else: # At least one domino can be connected to node
        length, weight = sorted(lenght_and_weight).pop()
        return length+1, weight + 2*node

with open('input') as f:
    edges = []
    for l in f:
        edges.append(tuple(map(int, l.rstrip().split('/'))))
    print('P1:', build_bridge(0, edges))
    print('P2:', get_longest_then_heaviest_bridge(0, edges)[1])


