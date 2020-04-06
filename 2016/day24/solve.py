#!/usr/bin/env python3

import argparse
import string
from collections import deque

class Robot:
    # Class variables:
    # - the maze map
    # - the number of items to collect
    def __init__(self, pos, items, steps):
        self.pos = pos
        self.items = items
        self.steps = steps

    def spawn(self, bfs, visited, end_item=None):
        i, j = self.pos
        for new_pos in [(i+1, j), (i-1, j), (i, j-1), (i, j+1)]:
            # Check that new_pos is in the maze
            ni, nj = new_pos
            if 0 <= ni < len(Robot.maze) and 0 <= nj < len(Robot.maze[0]):
                if maze[ni][nj] == '#':
                    continue
                elif maze[ni][nj] == '.':
                    robot = Robot(new_pos, self.items.copy(), self.steps + 1)
                elif maze[ni][nj] in string.digits:
                    items = self.items.copy()
                    items.add(maze[ni][nj])
                    robot = Robot(new_pos, items, self.steps + 1)
                else:
                    raise(Exception('You should not land here!'))
                if robot not in visited:
                    visited.add(robot)
                    bfs.appendleft(robot)

    def collected_all_items(self):
        return len(self.items) == Robot.num_items

    def is_home(self):
        return Robot.home == self.pos

    def __hash__(self):
        return hash(tuple( [ self.pos, tuple(self.items) ] ))

    def __repr__(self):
        return 'pos:{}, items:{}, steps:{}'.format(self.pos, self.items, self.steps)

    def __eq__(self, other):
        return hash(self) == hash(other)


def p(maze):
    # Count the number of items to collect
    # Find the initial position
    cnt = 0
    for i, s in enumerate(maze):
        for j, c in enumerate(s):
            if c == '0':
                init_i, init_j = i, j
                cnt += 1
            elif c in string.digits:
                cnt += 1
    # Init
    Robot.maze = maze
    Robot.num_items = cnt
    Robot.home = (init_i, init_j)
    robot = Robot((init_i, init_j), set('0'), 0)

    # Bread first search algorithm
    bfs = deque([ robot ]) 

    # Speed up:
    # Avoid visiting multiple times the same location with the same collected items
    visited = set()
    visited.add(robot)
    
    p1_found = False
    while len(bfs) > 0:
        robot = bfs.pop()
        if not p1_found and robot.collected_all_items():
            p1 = robot.steps
            p1_found = True
            robot.spawn(bfs, visited)
        elif robot.collected_all_items() and robot.is_home():
            return p1, robot.steps # P1 is always defined
        else:
            robot.spawn(bfs, visited)
    raise(Exception())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        maze = [ l.strip() for l in f ] 

    p1, p2 = p(maze)
    print('P1:', p1)
    print('P2:', p2)
