#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt

WIDTH=25
HEIGHT=6

def part1(layers):
    few_zero = min(layers, key = lambda x: np.count_nonzero(x == 0))
    return np.count_nonzero(few_zero == 1) * np.count_nonzero(few_zero == 2)

def pixel(l):
    for c in l:
        if c != 2:
            return c
    raise('Only transparent pixels')

def part2(layers):
    layers = np.apply_along_axis(pixel, 0, layers)
    plt.matshow(layers)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        layers = np.array(list(map(int, f.readline().rstrip())))

    layers = layers.reshape(-1, HEIGHT, WIDTH)
    print('part1: {}'.format(part1(layers)))
    part2(layers)
