#!/usr/bin/env python3

import argparse
import pprint
from itertools   import zip_longest
from collections import deque
from copy        import deepcopy

move_in_direction = {
        '>': lambda x, y: (x+1, y),
        '<': lambda x, y: (x-1, y),
        'v': lambda x, y: (x, y+1),
        '^': lambda x, y: (x, y-1),
        }

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        # self.direction.rotate()   -> turn right
        # self.direction.rotate(-1) -> turn left
        self.direction = deque(['>', '^', '<', 'v'])
        assert direction in self.direction
        while self.direction[0] is not direction:
            self.direction.rotate()
        self.next_turn = deque([-1, 0, 1])

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def move(self):
        # Move
        self.x, self.y = move_in_direction[self.direction[0]](self.x, self.y)

        # Rotate if needed
        c = maze[self.x][self.y]
        assert c in ( '+', '\\', '/', '-', '|' )
        d = self.direction[0]

        if c in [ '|', '-' ]:
            pass
        elif c is '/':
            if d in ('^', 'v'):
                self.direction.rotate()
            else:
                self.direction.rotate(-1)
        elif c is '\\':
            if d in ('^', 'v'):
                self.direction.rotate(-1)
            else:
                self.direction.rotate()
        elif c is '+':
            self.direction.rotate(self.next_turn[0])
            self.next_turn.rotate(-1)


def print_maze(carts, maze):
    print('='*80)
    print()
    copy_maze = [ list(col[:]) for col in maze ]

    for cart in carts:
        copy_maze[cart.x][cart.y] = cart.direction[0]

    # Display properly
    copy_maze = list(zip_longest(*copy_maze))
    for line in copy_maze:
        for char in line:
            print(char, end='')
        print()
    print()

def part1(carts, maze):
    carts = deepcopy(carts)
    carts_order = []
    carts_positions = set( (c.x, c.y) for c in carts)
    while True:
        #print(carts)
        #print(carts_order)
        #print(carts_positions)
        #print_maze(carts, maze)
        try:
            c = carts_order.pop()
        except IndexError:
            carts_order = sorted(carts, reverse=True)
            c = carts_order.pop()
        carts_positions.remove( (c.x, c.y) )
        c.move()
        if (c.x, c.y) in carts_positions:
            return c.x, c.y
        else:
            carts_positions.add( (c.x, c.y) )

def part2(carts, maze):
    carts_copy = deepcopy(carts)
    carts_order = []
    carts_positions = set( (c.x, c.y) for c in carts)
    while True:
        #print(carts_copy)
        #print(carts_order)
        #print(carts_positions)
        #print_maze(carts_copy, maze)
        try:
            c = carts_order.pop()
        except IndexError:
            carts_order = sorted(carts_copy, reverse=True)
            c = carts_order.pop()
        #print('selected cart: {},{} dir: {}'.format(c.x, c.y, c.direction[0]))
        carts_positions.remove( (c.x, c.y) )
        c.move()
        if (c.x, c.y) in carts_positions:
            # Collide the carts and remove them from our "state" variables
            carts_copy.remove(c)
            for d in carts_copy:
                if d.x == c.x and d.y == c.y:
                    carts_copy.remove(d)
                    try:
                        carts_order.remove(d)
                    except:
                        pass
            carts_positions.remove( (c.x, c.y) )
            # Last cart ?
            if len(carts_copy) == 1:
                c = carts_copy.pop()
                if len(carts_order) > 0:
                    c.move()
                return c.x, c.y
        else:
            carts_positions.add( (c.x, c.y) )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    # Get the maze
    with open(args.input) as f:
        maze = f.read().splitlines()
        maze = list(zip_longest(*maze, fillvalue = ' '))
        maze = [ list(x) for x in maze ]

    # Get the carts
    carts = []
    for x, col in enumerate(maze):
        for y, c in enumerate(col):
            # Append new cart
            if c in ( '<', '>', 'v', '^' ):
                new_cart = Cart(x, y, c)
                carts.append(new_cart)
                # Get the maze symbol underneath the cart
                if c in ( '<', '>' ):
                    maze[x][y] = '-'
                else:
                    maze[x][y] = '|'
    print('part1: {}, {}'.format(*part1(carts, maze)))
    print('part2: {}, {}'.format(*part2(carts, maze)))
