#!/usr/bin/env python3

import itertools
import argparse

def p2(freqs):
    cur_freq = 0
    previous_freqs = { cur_freq }
    for f in itertools.cycle(freqs):
        cur_freq += f
        if cur_freq in previous_freqs:
            return cur_freq
        else:
            previous_freqs.add(cur_freq)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        freqs = [ int(l.rstrip()) for l in f]
    print('P1:', sum(freqs))
    print('P2:', p2(freqs))
