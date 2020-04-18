#!/usr/bin/env python3

import argparse
from collections import deque
from lib.intcode import VM

class Droid_fun:
    NORTH=1
    SOUTH=2
    EAST=3
    WEST=4

    BACK = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: WEST,
            WEST: EAST,
            }

    def __init__(self, exe):
        self.vm = VM(exe)
        self.x = 0
        self.y = 0
        self.grid = {}
        self.grid[(0, 0)] = '.'

    def apply_move(self, d):
        if d == self.NORTH:
            return self.x, self.y+1
        elif d == self.SOUTH:
            return self.x, self.y-1
        elif d == self.WEST:
            return self.x-1, self.y
        elif d == self.EAST:
            return self.x+1, self.y

    def move(self, seq):
        for step in seq:
            self.vm.push_in(step)
            _ = next(self.vm.run())
            self.x, self.y = self.apply_move(step)

    def move_back(self, seq):
        back = [ self.BACK[step] for step in reversed(seq) ]
        self.move(back)

    def explore(self, d, seq, queue):
        if self.apply_move(d) in self.grid:
            return False

        # Run the vm to move
        self.vm.push_in(d)
        out = next(self.vm.run())

        if out == 0:
            # hit a wall
            self.grid[self.apply_move(d)] = '#'
        elif out == 1: 
            # empty square to be explored
            self.x, self.y = self.apply_move(d) # droid moved
            self.grid[(self.x, self.y)] = '.'
            new_seq = seq[:]
            new_seq.append(d)
            queue.appendleft(new_seq)
            # move backwards
            self.move_back([d])
        elif out == 2: 
            # oxygen found !
            return True
        else:
            raise Exception('Received out: {}'.format(out))
        return False

    def bfs(self):
        #
        # The easiest approach with how the droid works would be:
        #     - move the droid to explore all the grid with a dfs
        #     - run a bfs on the grid (without moving the droid)
        #
        # However since we are jedis, we are going to try to run a bfs.
        #
        # Since we are extra jedis we are doing so WITHOUT resetting the VM nor
        # instanciating several droids.
        #
        # It is unefficient but fun.
        # Life is fun.
        #
        queue = deque([]) # List of position to explore.
                          # Positions are represented by the sequence of instruction to get to the position (without failures)

        # Start at position (0, 0), reachable without running any steps
        queue.appendleft([])  # Empty list is how you reach position (0, 0)
        self.draw()

        while True:
            # Each time we enter this loop, we expect to be at (0, 0)
            if self.x != 0 or self.y != 0:
                raise

            # Go to the tip of the node by running the sequence
            seq = queue.pop()
            self.move(seq)

            # Explore all the directions
            for d in self.NORTH, self.SOUTH, self.WEST, self.EAST:
                # Explore function does not move the droid
                found = self.explore(d, seq, queue)
                if found:
                    return len(seq) + 1
                self.draw()

            # Go back to position (0, 0)
            self.move_back(seq)
        
    def draw(self):
        minx = min( [ x[0] for x in self.grid ] )
        maxx = max( [ x[0] for x in self.grid ] )
        miny = min( [ x[1] for x in self.grid ] )
        maxy = max( [ x[1] for x in self.grid ] )
        print('-'*80)
        print()
        for j in range(maxy+5, miny-5, -1):
            for i in range(minx-5, maxx+5):
                if self.x == i and self.y == j:
                    print('D', end='')
                else:
                    print(self.grid.get((i, j), ' '), end='')
            print()
        print()


class Droid_efficient:
    NORTH=1
    SOUTH=2
    EAST=3
    WEST=4

    BACK = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: WEST,
            WEST: EAST,
            }

    def __init__(self, exe):
        self.vm = VM(exe)
        self.x = 0
        self.y = 0
        self.grid = {}
        self.grid[(0, 0)] = '.'

    def apply_move(self, d, x=None, y=None):
        if x is None:
            x = self.x
            y = self.y
        if d == self.NORTH:
            return x, y+1
        elif d == self.SOUTH:
            return x, y-1
        elif d == self.WEST:
            return x-1, y
        elif d == self.EAST:
            return x+1, y

    def dfs(self):
        # Explore all the directions
        for d in self.NORTH, self.SOUTH, self.WEST, self.EAST:
            # Check if the direction is already visited
            if self.apply_move(d) in self.grid:
                continue

            # Run the vm to move
            self.vm.push_in(d)
            out = next(self.vm.run())

            if out == 0:
                # hit a wall
                self.grid[self.apply_move(d)] = '#'
            elif out == 1:
                self.x, self.y = self.apply_move(d) # droid moved
                self.grid[(self.x, self.y)] = '.'
                self.dfs()
                # Move back
                self.vm.push_in(self.BACK[d])
                _ = next(self.vm.run())
                self.x, self.y = self.apply_move(self.BACK[d])
            elif out == 2:
                self.x, self.y = self.apply_move(d) # droid moved
                self.grid[(self.x, self.y)] = 'o'
                self.dfs()
                # Move back
                self.vm.push_in(self.BACK[d])
                _ = next(self.vm.run())
                self.x, self.y = self.apply_move(self.BACK[d])
            else:
                raise Exception('Received out: {}'.format(out))

    def bfs_to_oxygen(self):
        # Init
        visited = set()
        queue = deque()
        alt_queue = deque()
        cnt = 1

        visited.add((0, 0))
        queue.appendleft((0, 0))
        while True:
            # Pop all elements from queue
            while queue:
                x, y = queue.pop()
                for d in self.NORTH, self.SOUTH, self.WEST, self.EAST:
                    nx, ny = self.apply_move(d, x, y)
                    if (nx, ny) in visited:
                        continue
                    else:
                        visited.add((nx, ny))
                    if self.grid[(nx, ny)] == '.':
                        alt_queue.appendleft((nx, ny))
                    elif self.grid[(nx, ny)] == 'o':
                        return cnt
            queue, alt_queue = alt_queue, queue
            cnt += 1

    def bfs_from_oxygen(self):
        # Init
        visited = set()
        queue = deque()
        alt_queue = deque()
        cnt = -1

        for k, v in self.grid.items():
            if v == 'o':
                break

        visited.add(k)
        queue.appendleft(k)
        while queue:
            # Pop all elements from queue
            while queue:
                x, y = queue.pop()
                for d in self.NORTH, self.SOUTH, self.WEST, self.EAST:
                    nx, ny = self.apply_move(d, x, y)
                    if (nx, ny) in visited:
                        continue
                    else:
                        visited.add((nx, ny))
                    if self.grid[(nx, ny)] == '.':
                        alt_queue.appendleft((nx, ny))
            queue, alt_queue = alt_queue, queue
            cnt += 1
        return cnt

    def draw(self):
        minx = min( [ x[0] for x in self.grid ] )
        maxx = max( [ x[0] for x in self.grid ] )
        miny = min( [ x[1] for x in self.grid ] )
        maxy = max( [ x[1] for x in self.grid ] )
        print('-'*80)
        print()
        for j in range(maxy+5, miny-5, -1):
            for i in range(minx-5, maxx+5):
                if self.x == i and self.y == j:
                    print('D', end='')
                else:
                    print(self.grid.get((i, j), ' '), end='')
            print()
        print()


def part1_fun(exe):
    droid = Droid_fun(exe)
    return droid.bfs()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        exe = list(map(int, f.readline().split(',')))

    droid = Droid_efficient(exe)
    droid.dfs()
    print('part1: {}'.format(droid.bfs_to_oxygen()))
    print('part2: {}'.format(droid.bfs_from_oxygen()))

