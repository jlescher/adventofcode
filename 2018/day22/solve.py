#!/usr/bin/env python3

import argparse
from math   import inf
from pprint import pprint
import heapq
import pdb

class mode_maze:
    MODULO  = 20183
    INDEX_X = 16807
    INDEX_Y = 48271
    # Values are significant
    NEITHER, TORCH, GEAR   = 0, 1, 2
    ROCKY  , WET  , NARROW = 0, 1, 2

    def __init__(self, depth, pos):
        self.depth  = depth
        self.target = pos
        self.grid   = {}

        # Get the erosion level of all the required coordinates
        self.erosion_levels = {}
        assert pos[0] > 0
        assert pos[1] > 1
        for x in range(0, pos[0]+1):
            for y in range(0, pos[1]+1):
                self.add_type((x, y))

    def add_type(self, pos):
        if pos not in self.erosion_levels:
            if pos == (0,0):
                self.erosion_levels[pos] = self.depth % mode_maze.MODULO
            elif pos == self.target:
                self.erosion_levels[pos] = self.depth % mode_maze.MODULO
            elif pos[0] == 0:
                self.erosion_levels[pos] = (pos[1] * mode_maze.INDEX_Y + self.depth) % mode_maze.MODULO
            elif pos[1] == 0:
                self.erosion_levels[pos] = (pos[0] * mode_maze.INDEX_X + self.depth) % mode_maze.MODULO 
            else:
                # Retry until it works
                while True:
                    try:
                        self.erosion_levels[pos] = (self.erosion_levels[ (pos[0]-1, pos[1]) ] * self.erosion_levels[ (pos[0], pos[1]-1) ] + self.depth) % mode_maze.MODULO
                    except KeyError as e:
                        # Recursively add the dependencies that we need
                        self.add_type(e.args[0])
                    else:
                        break
        level = self.erosion_levels[pos] % 3
        self.grid[pos] = level

    def is_tool_allowed(self, pos, tool):
        return self.grid[pos] != tool

    def dijkstra(self):
        # Init
        P = set()
        dist = []
        heapq.heappush(dist, (0, (0, 0), mode_maze.TORCH))

        while True:
            # Select the vertex with the smallest distance
            d, pos, tool = heapq.heappop(dist)

            # Check for target
            if pos == self.target and tool == mode_maze.TORCH:
                return d

            # Check pos is new
            if (pos, tool) in P:
                continue

            P.add((pos, tool))

            # Update neighbours
            for new_pos in ( (pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1) ):
                if new_pos[0] < 0 or new_pos[1] < 0:
                    continue
                # Make sure the erosion level is available
                if new_pos not in self.erosion_levels:
                    self.add_type(new_pos)
                if self.is_tool_allowed(new_pos, tool) and (new_pos, tool) not in P:
                    heapq.heappush(dist, (d+1, new_pos, tool))

            # Change tool
            for new_tool in (mode_maze.NEITHER, mode_maze.TORCH, mode_maze.GEAR):
                if tool != new_tool and self.is_tool_allowed(pos, new_tool) and (pos, new_tool) not in P:
                    heapq.heappush(dist, (d+7, pos, new_tool))

    def get_risk_level(self):
        return sum ( v for k, v in self.grid.items() if 0 <= k[0] <= self.target[0] and 0 <= k[1] <= self.target[1] )

    def __str__(self):
        s = ''
        for y in range(0, self.target[1] + 1 + 5):
            for x in range(0, self.target[0] + 1 + 5):
                pos = (x,y)
                if pos == (0,0):
                    s += 'M'
                elif pos == self.target:
                    s += 'T'
                else:
                    if pos not in self.grid:
                        self.add_type(pos)
                    s += ('.', '=', '|', ' ')[self.grid.get(pos, 3)]
            s += '\n'
        return s

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        depth = int(f.readline().rstrip().split(' ')[1])
        pos   = tuple(map(int, f.readline().rstrip().split(' ')[1].split(',')))

    m = mode_maze(depth, pos)
    print(m)
    print('part1: {}'.format(m.get_risk_level()))
    print('part2: {}'.format(m.dijkstra()))
