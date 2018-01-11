#!/usr/bin/env python3

import re
from collections import Counter

# Storing the node as a list instead of a dictionnary would have made things easier.
# Using a `class Node` would have been even better.

def explore_node(node_name, graph):
    for sub in graph[node_name][1]:
        unbalanced_found, weight = explore_node(sub, graph)
        if unbalanced_found:
            return True, weight
    # Check if the tower is balanced
    try:
        subnode_weights = [ graph[sub][2] for sub in graph[node_name][1] ]
    except IndexError as e:
        print('asdf')
    counter = Counter(subnode_weights)
    if len(counter) == 0 or len(counter) == 1: # balanced
        pass
    elif len(counter) == 2: # unbalanced
        for w, cnt in counter.items():
            if cnt == 1:
                bad_weight = w
            else:
                good_weight = w
        diff = good_weight - bad_weight
        # Find the bad program
        for sub in graph[node_name][1]:
            if graph[sub][2] == bad_weight:
                return  True, graph[sub][0] + diff
    else:
        raise(Exception('Should not land here: more than one program is unbalanced'))
    # dict[node_name] = [ weight, [ subnodes ], total_weight ]
    graph[node_name].append(graph[node_name][0])
    for sub in graph[node_name][1]:
        graph[node_name][2] += graph[sub][2]
    return False, None

def find_root(graph):
    nodes = [ x for x in graph.keys() ]
    for node in graph.values():
        for sub in node[1]:
            try:
                nodes.remove(sub)
            except ValueError:
                pass
    return nodes.pop()

with open('input') as f:
    graph = {}
    pattern = re.compile('(?P<node>\w+)\s+\((?P<weight>\d+)\)\s+(?:->\s+)?(?P<subnodes>.*)?')
    for l in f:
        match = pattern.match(l.replace(',', ''))
        node, weight, subnodes = match.group('node'), int(match.group('weight')), match.group('subnodes').replace(',', '').split()
        graph[node] = [ weight, subnodes]
    root = find_root(graph)
    print('P1:', root)
    print('P2:', explore_node(root, graph)[1])


