#!/usr/bin/env python3

import argparse
from pprint      import pprint
from copy        import deepcopy

def display_grid(symbol, l, grid):
    grid_copy = deepcopy(grid)
    for x,y in l:
        grid_copy[x][y] = symbol
    for line in grid_copy:
        for c in line:
            print(c, end='')
        print()
    print()

def display(rounds, beings, grid):
    print('='*80)
    print('after {} rounds'.format(rounds))
    display_grid('', [], grid)
    for b in beings:
        print(b)
    print('-'*80)
    pass

def get_adjacent_squares(x, y):
    return ( (x-1, y), (x+1, y), (x, y-1), (x, y+1) )

def bfs(x, y, in_range, grid):
    ######## Init

    # Keys are visited squares, values are the best first move to reach the visited square
    visited = { (x,y): (None, None) }
    queue = [ (x, y) ]
    alt_queue = []

    ######## bfs
    nearest = []
    keep_exploring = True
    while keep_exploring and len(queue) > 0:
        while queue:
            x,y = queue.pop()

            # Are we in an in_range position ?
            if (x, y) in in_range:
                keep_exploring = False # Finish processing the current queue but stop exploring
                nearest.append((x, y))
                continue
            if keep_exploring:
                # Explore the 4 directions
                for i, j in get_adjacent_squares(x, y):
                    firstmove_x, firstmove_y = visited[(x,y)]
                    if grid[i][j] == '.': # Make sure the square is available
                        if (i, j) in visited: 
                            # The square has already been marked as visited
                            # The square has been already been added to alt_queue for further exploration
                            # We might need to update the firstmove
                            visited[(i,j)] = min(visited[(i,j)], (firstmove_x, firstmove_y))
                        else:
                            # Mark the square as visited
                            # Record the firstmove to reach that square
                            visited[(i,j)] = (firstmove_x, firstmove_y) if firstmove_x else (i,j)
                            alt_queue.append((i,j))
        queue = alt_queue
        alt_queue = []

    if nearest:
        chosen = sorted(nearest)[0]
        #display_grid('!', nearest, grid)
        #display_grid('+', [ chosen ], grid)
        #print(visited[chosen])
        return visited[chosen]
    else:
        return None, None


class Being:
    def __init__(self, t, x, y, attack_power):
        # t stands for type which is a reserved word
        self.t  = t
        self.x  = x
        self.y  = y
        self.hp = 200
        self.attack_power = attack_power if self.t is 'E' else 3
        self.enemy = 'G' if self.t is 'E' else 'E'

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def __str__(self):
        return '{} at ({},{}) hp={}'.format(self.t, self.x, self.y, self.hp)

    def get_targets(self, beings):
        return [ b for b in beings if b.t == self.enemy and b.hp > 0 ]

    def get_adjacent_squares(self):
        return get_adjacent_squares(self.x, self.y)

    def is_dead(self):
        return self.hp <= 0

    def move(self, beings, grid):
        # List all possible targets
        targets = self.get_targets(beings)

        # Make sure there is at least one target
        if not targets:
            return False

        # Get in range squares
        in_range = [ (x, y) for t in targets for x,y in t.get_adjacent_squares() ]

        # Check if self is already in range, if so no need to move
        if (self.x, self.y) in in_range: 
            return True

        # Get the AVAILABLE in range squares
        in_range = [ (x, y) for x,y in in_range if grid[x][y] == '.']

        # No AVAILABLE in range squares go to next being
        if not in_range:
            return True

        # Get where to move
        new_x, new_y = bfs(self.x, self.y, in_range, grid)

        # Move
        if new_x != None and new_y != None:
            grid[self.x][self.y] = '.'
            self.x = new_x
            self.y = new_y
            grid[self.x][self.y] = self.t

        return True

    def receive_hit(self, attack_power, beings, grid):
        self.hp -= attack_power
        if self.hp <= 0:
            grid[self.x][self.y] = '.'

    def attack(self, beings, grid):
        # List all possible targets
        targets = [ t for t in self.get_targets(beings) if (t.x, t.y) in self.get_adjacent_squares() ]

        # Get the target
        if not targets:
            return
        
        min_hp = min(list(map(lambda t: t.hp, targets)))
        targets_fewest_hp = [ t for t in targets if t.hp == min_hp ]
        t = sorted(targets_fewest_hp)[0]

        # Hit t
        t.receive_hit(self.attack_power, beings, grid)


def init_beings(attack_power, grid):
    beings = []
    for x, line in enumerate(grid):
        for y, c in enumerate(line):
            if c in ['G', 'E']:
                being = Being(c, x, y, attack_power)
                beings.append(being)
    beings.sort()
    return beings


def part1(grid):
    grid = deepcopy(grid)
    beings = init_beings(3, grid)

    rounds = 0
    remain_targets = True
    #display(rounds, beings, grid)
    while remain_targets:
        # Action
        for b in beings:
            if not b.is_dead():
                remain_targets = b.move(beings, grid)
                b.attack(beings, grid)

        # Update the new being list
        beings = [ b for b in beings if not b.is_dead() ]
        beings.sort()
        if remain_targets:
            rounds += 1

    return rounds * sum(b.hp for b in beings)


def run_part2(attack_power, grid):
    grid = deepcopy(grid)
    beings = init_beings(attack_power, grid)

    rounds = 0
    remain_targets = True
    #display(rounds, beings, grid)
    while remain_targets:
        # Perform a round
        for b in beings:
            if not b.is_dead():
                remain_targets = b.move(beings, grid)
                b.attack(beings, grid)

        # Check if an elf died
        if len([b for b in beings if b.t == 'E' and b.is_dead()]) > 0:
            return False, 0

        # Update the new being list
        beings = [ b for b in beings if not b.is_dead() ]
        beings.sort()
        if remain_targets:
            rounds += 1
            #display(rounds, beings, grid)

    #display(rounds, beings, grid)
    return True, rounds * sum(b.hp for b in beings)


def part2(grid):
    # We cannot assume that the higher the elf's attack power is, the best chance of survival they have.
    # Killing an enemy faster could result in arriving in an opened position where an elf is surrounded by enemies.
    attack_power = 3
    success = False

    while not success and attack_power <= 200:
        success, score = run_part2(attack_power, grid)
        attack_power += 1

    return score


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    # Get the grid
    with open(args.input) as f:
        grid = f.read().splitlines()
        grid = [ list(x) for x in grid ]

    print('part1: {}'.format(part1(grid)))
    print('part2: {}'.format(part2(grid)))
