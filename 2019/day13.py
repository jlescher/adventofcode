#!/usr/bin/env python3

import argparse
from collections import defaultdict
from lib.intcode import VM
from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class Arcade:
    EMPTY  = 0
    WALL   = 1
    BLOCK  = 2
    PADDLE = 3
    BALL   = 4

    LEFT=-1
    STILL=0
    RIGHT=1

    def __init__(self, exe):
        self.vm = VM(exe)
        self.tiles = defaultdict(lambda: self.EMPTY)
        self.score = None
        self.paddle = None # track paddle horizontal component separately
        self.ball = None   # track ball horizontal component separately

    def send_joystick(self):
        #self.draw()
        if self.ball > self.paddle:
            self.vm.push_in(self.RIGHT)
        elif self.ball < self.paddle:
            self.vm.push_in(self.LEFT)
        else:
            self.vm.push_in(self.STILL)

    def play(self):
        while True:
            try:
                x = next(self.vm.run())
                if x is None: # vm is waiting for an input
                    self.send_joystick()
                    continue
                y = next(self.vm.run())
                z = next(self.vm.run())
            except StopIteration:
                break
            # Set score
            if x == -1 and y == 0:
                self.score = z
            else: 
                # Register tile
                self.tiles[(x, y)] = z

                # Track ball
                if z == self.BALL:
                    self.ball = x
                    # Check if there are still blocks
                    if not self.BLOCK in self.tiles.values():
                        break

                # Track paddle
                if z == self.PADDLE:
                    self.paddle = x

        return self.score


    def draw(self):
        minx = min( [ x[0] for x in self.tiles ] )
        maxx = max( [ x[0] for x in self.tiles ] )
        miny = min( [ x[1] for x in self.tiles ] )
        maxy = max( [ x[1] for x in self.tiles ] )
        print('-' * 80 )
        print()
        for y in range(miny, maxy+1):
            for x in range(minx, maxx+1):
                print(self.tiles[(x,y)], end='')
            print()
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        exe = list(map(int, f.readline().split(',')))

    vm = VM(exe).run()
    cnt = 0
    for _, _, tid in grouper(vm, 3):
        if tid == Arcade.BLOCK:
            cnt += 1
    print('part1: {}'.format(cnt))

    exe[0] = 2 # insert a coin
    arcade = Arcade(exe)
    score = arcade.play()
    print('part2: {}'.format(score))
