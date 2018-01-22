#!/usr/bin/env python3

from collections import deque
from itertools import combinations, chain
import pdb

floors_P1 = [ 
        [ 'PG', 'TG', 'TM', 'XG', 'RG', 'RM', 'CG', 'CM' ],
        [ 'PM', 'XM' ],
        [],
        []
        ]

floors_P2 =  [
        [ 'PG', 'TG', 'TM', 'XG', 'RG', 'RM', 'CG', 'CM', 'EG', 'EM', 'DG', 'DM'],
        [ 'PM', 'XM' ],
        [],
        []
        ]

def floor_has_generator(floor):
    for e in floor:
        if e[1] == 'G':
            return True
    return False

def floor_is_safe(floor):
    if not floor_has_generator(floor):
        return True
    else:
        for e in floor:
            if e[1] == 'M':
                if e[0] + 'G' not in floor:
                    return False
        return True


class Floors():
    def __init__(self, level, num_moves, floors):
        self.level = level
        self.num_moves = num_moves
        self.floors = []
        for f in floors:
            self.floors.append(f[:]) # Copy 
    def floors_are_safe(self):
        for f in self.floors:
            if not floor_is_safe(f):
                return False
        return True

    def end(self):
        if len(self.floors[0]) + len(self.floors[1]) + len(self.floors[2]) == 0:
            return True
        return False

    def move(self, elements, level_src, level_dst):
        assert(self.level == level_src)
        if not floor_is_safe(elements):
            return False
        for e in elements:
            self.floors[level_src].remove(e)
            self.floors[level_dst].append(e)
        self.level = level_dst
        self.num_moves += 1
        return self.floors_are_safe()

    def spawn(self, bfs, known_states):
        next_levels = [ x for x in [self.level + 1,  self.level - 1] if x in [0, 1, 2, 3] ]
        for next_level in next_levels:
            for e in chain(
                    combinations(self.floors[self.level], 1),
                    combinations(self.floors[self.level], 2)
                    ):
                # Fork self
                new_floors = Floors(self.level, self.num_moves, self.floors)
                # Apply the move 
                add_to_bfs = new_floors.move(e, self.level, next_level)
                if add_to_bfs and new_floors not in known_states:
                    bfs.appendleft(new_floors)
                    known_states.add(new_floors)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        string = 'moves:{}\n'.format(self.num_moves)
        for i, f in enumerate(reversed(self.floors)):
            string += 'F{} {} {}\n'.format(len(self.floors) - i, 'E' if self.level == (len(self.floors)-1-i) else '.', f)
        return string

    def __str__(self):
        string = 'moves:{}\n'.format(self.num_moves)
        for i, f in enumerate(reversed(self.floors)):
            string += 'F{} {} {}\n'.format(len(self.floors) - i, 'E' if self.level == (len(self.floors)-1-i) else '.', f)
        return string
    
    def __hash__(self):
        string = str(self.level)
        dict_elem = {}
        for i, f in enumerate(self.floors):
            for e0, e1 in f:
                if e1 == 'M':
                    dict_elem[e0] = (dict_elem.setdefault(e0, (10, 10))[0], i)
                else:
                    dict_elem[e0] = (i, dict_elem.setdefault(e0, (10, 10))[1])
        vals = tuple([ self.level ] + list(sorted(dict_elem.values())))
        return hash(vals)


def j11(floors):
    init = Floors(0, 0, floors)
    bfs = deque([])
    bfs.appendleft(init)
    known_states  = set([init])

    # BFS 
    found = False
    while not found and len(bfs) > 0:
        state = bfs.pop()
        found = state.end()
        state.spawn(bfs, known_states)
    return state.num_moves

if __name__ == '__main__':
    print('P1:', j11(floors_P1))
    print('P2:', j11(floors_P2))
