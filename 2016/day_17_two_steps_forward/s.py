#!/usr/bin/env python3

from collections import deque
import hashlib
import string

INPUT='qzthpkfp'

def U(pos):
    return pos[0] - 1, pos[1]

def D(pos):
    return pos[0] + 1, pos[1]
def L(pos):
    return pos[0], pos[1] - 1

def R(pos):
    return pos[0], pos[1] + 1

direction = {
        'U':U,
        'D':D,
        'L':L,
        'R':R,
        }

class Square:
    def __init__(self, pos, path):
        self.pos = pos
        self.path = path

    def end(self): 
        return self.pos == (3, 3)

    def spawn(self, bfs):
        h = hashlib.md5(self.path.encode()).hexdigest()
        for d, c in zip('UDLR', h):
            if c in string.ascii_lowercase[1:]:
                new_pos = direction[d](self.pos)
                if 0 <= new_pos[0] <= 3 and 0 <= new_pos[1] <= 3: # In grid
                    new_square = Square(new_pos, self.path + d)
                    bfs.appendleft(new_square)

def p1():
    # Queue, appendleft() and pop()
    bfs = deque([])
    bfs.appendleft(Square((0, 0), INPUT))
    while len(bfs) > 0:
        s = bfs.pop()
        if s.end():
            break
        s.spawn(bfs)
    return s.path[len(INPUT):]


def p2():
    # Queue, appendleft() and pop()
    bfs = deque([])
    bfs.appendleft(Square((0, 0), INPUT))
    max_steps = 0
    while len(bfs) > 0:
        s = bfs.pop()
        if s.end():
            steps = len(s.path) - len(INPUT)
            max_steps = steps if steps > max_steps else max_steps
            continue
        s.spawn(bfs)
    return max_steps

if __name__ == '__main__':
    print('P1:', p1())
    print('P2:', p2())

