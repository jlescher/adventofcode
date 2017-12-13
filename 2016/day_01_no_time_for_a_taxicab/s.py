#!/usr/bin/env python3

def rotate(pos, direction):
    if direction == 'L':
        pos[2] = pos[2] - 1
    else:
        pos[2] = pos[2] + 1
    pos[2] = pos[2] % 4

def walk(pos, step, saved_pos):
    for i in range(step):
        if pos[2] == 0:
            pos[1] += 1
        elif pos[2] == 1:
            pos[0] += 1
        elif pos[2] == 2:
            pos[1] -= 1
        else:
            pos[0] -= 1
        cur_pos = (pos[0], pos[1])
        if cur_pos in saved_pos:
            return True, cur_pos
        else:
            saved_pos.add(cur_pos)
    return False, None

with open('input') as f:
    saved_pos = { (0, 0) }
    pos = [0,0,0]
    instructions = f.read().rstrip().split(', ')
    for ins in instructions:
        direction = ins[0]
        step = int(ins[1:])
        rotate(pos, direction)
        ret = walk(pos, step, saved_pos)
        if ret[0]:
            print(ret[1])
            print(abs(ret[1][0]) + abs(ret[1][1]))
            break
