#!/usr/bin/env python3

# Not very proud of this solution.
with open('input') as f:
    # Dictionnary keys are the graph nodes, values represent a connected component number 
    connected_components = {}
    for l in f.readlines():
        a = l.rstrip().split()
        left_node, right_nodes = (lambda x: (x[0], x[2:]))(l.rstrip().replace(',', '').split())
        if left_node not in connected_components.keys(): # .keys() is optional here but I like it
            connected_components[left_node] = left_node
        left_cc = connected_components[left_node]
         
        for node in right_nodes:
            if node in connected_components.keys(): # merge node's and left_node's connected components
                node_cc = connected_components[node]
                for point, cc in connected_components.items():
                    if cc == node_cc:
                        connected_components[point] = left_cc
            else:
                connected_components[node] = left_cc

    print('programs PID0\'s group: {}'.format(list(connected_components.values()).count(connected_components['0'])))
    print('number of groups: {}'.format(len(set(connected_components.values()))))
    
