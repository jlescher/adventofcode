#!/usr/bin/env python3

import argparse
from collections import deque
from lib.intcode import VM
import matplotlib.pyplot as plt

class Robot:
    BLACK = 0
    WHITE = 1

    move = {
            '^': lambda x, y: (x  , y-1),
            '>': lambda x, y: (x+1, y  ),
            'v': lambda x, y: (x  , y+1),
            '<': lambda x, y: (x-1, y  ),
            }

    def __init__(self, color, exe):
        super(Robot, self).__init__()
        self.pos = (0,0)
        self.direction = deque([ '^', '<', 'v', '>' ])
        self.panel = {}
        self.panel[self.pos] = color
        self.vm = VM(exe)

    def paint(self):
        while True:
            try:
                self.vm.push_in(self.panel.get(self.pos, self.BLACK))
                color = next(self.vm.run())
                direc = next(self.vm.run())
            except StopIteration:
                break

            # Paint
            self.panel[self.pos] = color
            # Turn
            if direc == 0:
                self.direction.rotate(-1)
            else:
                self.direction.rotate(1)
            # Move
            self.pos = self.move[self.direction[0]](*self.pos)

    def get_num_painted(self):
        return len(self.panel)

    def draw(self):
        minx = min([ x[0] for x in self.panel ])
        maxx = max([ x[0] for x in self.panel ])
        miny = min([ x[1] for x in self.panel ])
        maxy = max([ x[1] for x in self.panel ])
        hull = []
        for y in range(miny, maxy+1):
            hull.append( [ self.panel.get((x, y), 0) for x in range(minx, maxx+1) ])
        plt.matshow(hull)
        plt.show()

def part2(exe):
    robot = Robot(Robot.WHITE, exe)
    robot.paint()
    robot.draw()

def part1(exe):
    robot = Robot(Robot.BLACK, exe)
    robot.paint()
    return robot.get_num_painted()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        exe = list(map(int, f.readline().split(',')))

    print('part1: {}'.format(part1(exe)))
    part2(exe)
