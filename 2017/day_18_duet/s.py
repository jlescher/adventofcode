#!/usr/bin/env python3

from collections import deque
from pprint import pprint

hw = {
        0: { 'pc': 0, 'registers' : {'p' : 0}, 'rcv' : deque([])},
        1: { 'pc': 0, 'registers' : {'p' : 1}, 'rcv' : deque([]), 'snd_count': 0}
}


def get_val(proc, x):
    try:
        return int(x)
    except ValueError:
        return hw[proc]['registers'].get(x, 0)


def snd(proc, x):
    if proc == 1:
        hw[1]['snd_count'] += 1
    hw[(proc+1) % 2]['rcv'].appendleft(get_val(proc, x))
    hw[proc]['pc'] += 1


def _set(proc, x, y):
    hw[proc]['registers'][x] = get_val(proc,y)
    hw[proc]['pc'] += 1


def add(proc, x, y):
    hw[proc]['registers'][x] = get_val(proc, x) + get_val(proc, y)
    hw[proc]['pc'] += 1


def mul(proc, x, y):
    hw[proc]['registers'][x] = get_val(proc, x) * get_val(proc, y)
    hw[proc]['pc'] += 1


def mod(proc, x, y):
    hw[proc]['registers'][x] = get_val(proc, x) % get_val(proc, y)
    hw[proc]['pc'] += 1


def rcv(proc, x):
    try:
        e = hw[proc]['rcv'].pop()
    except IndexError:
        pass
    else:
        hw[proc]['registers'][x] = e
        hw[proc]['pc'] += 1


def jgz(proc, x, y):
    if get_val(proc, x) > 0:
        hw[proc]['pc'] += get_val(proc, y)
    else:
        hw[proc]['pc'] += 1


ins = {
        'snd': snd,
        'set': _set,
        'add': add,
        'mul': mul,
        'mod': mod,
        'rcv': rcv,
        'jgz': jgz,
        }


def run(proc):
    saved_line = hw[proc]['pc']
    instruction = prog[hw[proc]['pc']]
    #print('[{}]: {}'.format(proc, instruction))
    ins[instruction[0]](proc, *instruction[1:])
    #print('[{}]'.format(proc), end = '')
    #pprint(hw[proc]['registers'])
    if saved_line == hw[proc]['pc']:
        return False
    return True

with open('input') as f:
    prog = [ x.rstrip().split(' ') for x in f ]
    # Poor man's threading
    # TODO: Look into python threading some day
    while run(0) or run(1) or run(0):
        pass
    print(hw[1]['snd_count'])
