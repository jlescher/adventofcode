#!/usr/bin/env python3

import argparse
from itertools import chain

move_door = {
        'N': lambda pos: (pos[0]-1, pos[1]),
        'S': lambda pos: (pos[0]+1, pos[1]),
        'W': lambda pos: (pos[0],   pos[1]-1),
        'E': lambda pos: (pos[0],   pos[1]+1),
        }

move_room = {
        'N': lambda pos: (pos[0]-2, pos[1]),
        'S': lambda pos: (pos[0]+2, pos[1]),
        'W': lambda pos: (pos[0],   pos[1]-2),
        'E': lambda pos: (pos[0],   pos[1]+2),
        }

def get_doors(pos):
    return ( (pos[0]-1, pos[1]),(pos[0]+1, pos[1]), (pos[0], pos[1]-1),   (pos[0], pos[1]+1) )

class Facility:
    def __init__(self):
        self.doors = set()
        self.rooms = set()
        self.cur_pos = (0, 0)
        self.rooms.add(self.cur_pos)

    def trace(self, regex):
        pos = self.cur_pos
        branch_stack = []
        for char in regex:
            if char == '^':
                pass
            elif char == '$':
                pass
            elif char in ('N', 'S', 'E', 'W'):
                self.doors.add( move_door[char](pos) )
                pos = move_room[char](pos)
                self.rooms.add(pos)
            elif char == '(':
                branch_stack.append(pos)
            elif char == '|':
                pos = branch_stack[-1]
            elif char == ')':
                branch_stack.pop()
                pass
            else:
                raise Exception('Unknown symbol: {}'.format(char))

    def find_furthest_room(self):
        steps = 0
        cnt_doors = 0
        rooms_visited = set()
        rooms_reached = set()
        rooms_reached.add( (0,0) )
        # At least one room has not been visited
        while rooms_visited != self.rooms:
            steps += 1
            # Explore each each rooms_reached
            new_rooms_reached = set()
            for room in rooms_reached:
                # Explore each direction
                for d in ('N', 'S', 'W', 'E'):
                    if move_door[d](room) in self.doors:
                        new_room = move_room[d](room)
                        if new_room not in rooms_visited:
                            if steps >= 1000:
                                cnt_doors += 1
                            new_rooms_reached.add(new_room)
                            rooms_visited.add(new_room)
            rooms_reached = new_rooms_reached
        return steps, cnt_doors

    def __str__(self):
        x_min = min(pos[0] for it in (self.rooms, self.doors) for pos in it)
        x_max = max(pos[0] for it in (self.rooms, self.doors) for pos in it)
        y_min = min(pos[1] for it in (self.rooms, self.doors) for pos in it)
        y_max = max(pos[1] for it in (self.rooms, self.doors) for pos in it)
        s = ''
        for i in range(x_min-1, x_max+2):
            for j in range(y_min-1, y_max+2):
                if (i, j) == self.cur_pos:
                    s += 'X'
                elif (i,j) in self.rooms:
                    s += '.'
                elif (i,j) in self.doors:
                    if i%2 == 0:
                        s += '|'
                    else:
                        s += '-'
                else:
                    s += '#'
            s += '\n'
        return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        regex = f.readline().rstrip()

    f = Facility()
    f.trace(regex)
    steps, cnt_doors = f.find_furthest_room()
    print('part1: {}'.format(steps))
    print('part2: {}'.format(cnt_doors))
