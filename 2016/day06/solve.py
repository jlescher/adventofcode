#!/usr/bin/env python3

import argparse
from collections import Counter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        messages = f.readlines()

    messages = [ x.rstrip() for x in messages ]

    letters = [ Counter(x).most_common(1).pop()[0] for x in zip(*messages) ]
    print('P1:', ''.join(letters))

    letters = [ Counter(x).most_common().pop()[0] for x in zip(*messages) ]
    print('P2:', ''.join(letters))

    

