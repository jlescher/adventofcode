#!/usr/bin/env python3

from collections import deque
import argparse, sys, os
sys.path.append(os.path.dirname(os.getcwd()))
from day09 import solve as day09
import matplotlib.pyplot as plt


class Robot(day09.VM):
    BLACK = 0
    WHITE = 1

    move = {
            '^': lambda x, y: (x  , y-1),
            '>': lambda x, y: (x+1, y  ),
            'v': lambda x, y: (x  , y+1),
            '<': lambda x, y: (x-1, y  ),
            }

    def __init__(self, start_color, prog):
        super(Robot, self).__init__()
        self.pos = (0,0)
        self.direction = deque([ '^', '<', 'v', '>' ])
        self.panel = {}
        self.panel[self.pos] = start_color
        self.start_paint = False # Mark as true if we paint (0,0)
        self.paint = True # output toggle
        self.reset_memory(prog)

    def _input(self, a):
        self.memory[a] = self.panel.get(self.pos, self.BLACK)

    def output(self, a):
        if self.paint:
            self.panel[self.pos] = self.memory[a]
            if not self.start_paint and self.pos == (0,0):
                self.start_color = True
        else:
            # Turn
            if self.memory[a] == 0:
                self.direction.rotate(-1)
            else:
                self.direction.rotate(1)
            # Move
            self.pos = self.move[self.direction[0]](*self.pos)
        self.paint ^= True

    def get_num_painted(self):
        return len(self.panel) if self.start_paint else len(self.panel) - 1

def run(start_color, prog):
    robot = Robot(start_color, prog)
    robot.execute()
    return robot

def part2(prog):
    panel = run(Robot.WHITE, prog).panel
    mini = min(panel, key = lambda x: x[0])[0]
    maxi = max(panel, key = lambda x: x[0])[0]
    minj = min(panel, key = lambda x: x[1])[1]
    maxj = max(panel, key = lambda x: x[1])[1]
    hull = []
    for j in range(minj, maxj+1):
        hull.append( [ panel.get((i, j), 0) for i in range(mini, maxi+1) ])
    plt.matshow(hull)
    plt.show()

def part1(prog):
    return run(Robot.BLACK, prog).get_num_painted()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = list(map(int, f.readline().split(',')))

    print('part1: {}'.format(part1(prog)))
    part2(prog)
