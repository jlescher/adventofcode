#!/usr/bin/env python3


import argparse

# Ugly code, please don't look at it

PASSWD_P1 = list('abcdefgh')
PASSWD_P2 = list('fbgdceah')


def swap_pos(l, m, n):
    l[m], l[n] = l[n], l[m]
    return l


def swap_letter(l, char0, char1):
    m, n = l.index(char0), l.index(char1)
    swap_pos(l, m, n)
    return l


def rotate_left(l, step):
    return l[step:] + l[:step]


def rotate_right(l, step):
    return rotate_left(l, -step)


def rotate_pos(l, d, step):
    if d == 'right':
        return rotate_right(l, step)
    else:
        return rotate_left(l, step)


def rotate_letter(l, char):
    ix = l.index(char)
    l = rotate_right(l, 1)
    l = rotate_right(l, ix)
    if ix >= 4:
        l = rotate_right(l, 1)
    return l

def rev_rotate_letter(l, char):
    '''
    Assumes there are 8 elements in the list
    List all the rotations to find the mapping.
    '''
    ix = l.index(char)
    if ix == 1:
        return rotate_left(l, 1)
    elif ix == 3:
        return rotate_left(l, 2)
    elif ix == 5:
        return rotate_left(l, 3)
    elif ix == 7:
        return rotate_left(l, 4)
    elif ix == 2:
        return rotate_right(l, 2)
    elif ix == 4:
        return rotate_right(l, 1)
    elif ix == 6:
        return l
    elif ix == 0:
        return rotate_left(l, 1)
    else:
        raise(Exception('Should not land here'))

def rev_move_pos(l, x, y):
    return move_pos(l, y, x)

def reverse_pos(l, x, y):
    x, y = min(x, y), max(x, y)
    sub = l[x:y+1]
    sub.reverse()
    return l[:x] + sub + l[y+1:]


def move_pos(l, x, y):
    e = l.pop(x)
    l.insert(y, e)
    return l


def parse(passwd, instructions):
    for x in instructions:
        if x[0] == 'swap' and x[1] == 'position':
            passwd = swap_pos(passwd, int(x[2]), int(x[5]))
        elif x[0] == 'swap' and x[1] == 'letter':
            passwd = swap_letter(passwd, x[2], x[5])
        elif x[0] == 'reverse':
            passwd = reverse_pos(passwd, int(x[2]), int(x[4]))
        elif x[0] == 'rotate' and x[1] in ('left', 'right'):
            passwd = rotate_pos(passwd, x[1], int(x[2]))
        elif x[0] == 'rotate':
            passwd = rotate_letter(passwd, x[6])
        elif x[0] == 'move':
            passwd = move_pos(passwd, int(x[2]), int(x[5]))
        else:
            raise(Exception('Unknown instruction'))
    return ''.join(passwd)


def rev_parse(passwd, instructions):
    instructions = instructions[::-1]
    for x in instructions:
        if x[0] == 'swap' and x[1] == 'position': # OK!
            passwd = swap_pos(passwd, int(x[2]), int(x[5]))
        elif x[0] == 'swap' and x[1] == 'letter': # OK!
            passwd = swap_letter(passwd, x[2], x[5])
        elif x[0] == 'reverse': # OK !
            passwd = reverse_pos(passwd, int(x[2]), int(x[4]))
        elif x[0] == 'rotate' and x[1] in ('left', 'right'):
            d = 'left' if x[1] == 'right' else 'right'
            passwd = rotate_pos(passwd, d, int(x[2]))
        elif x[0] == 'rotate':
            passwd = rev_rotate_letter(passwd, x[6])
        elif x[0] == 'move':
            passwd = rev_move_pos(passwd, int(x[2]), int(x[5]))
        else:
            raise(Exception('Unknown instruction'))
    return ''.join(passwd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        instructions = f.readlines()
    instructions = [ x.rstrip().split(' ') for x in instructions ]
    print('P1:', parse(PASSWD_P1, instructions))
    print('P2:', rev_parse(PASSWD_P2, instructions))
