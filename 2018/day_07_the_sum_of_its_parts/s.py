#!/usr/bin/env python3

from collections import defaultdict
from pprint import pprint
import argparse
import re

#
# Maintain two dictionnaries:
#
# 1. req['I'] = {'J', 'W'}
# Track which steps are required.
#
# 2. rev['J'] = { 'I' }
# Reverse dictionnary.
#

def p1(req, rev):
    # Find all steps that do not require a req.
    string = ''
    available = [ *set(rev).difference(set(req)) ]
    available = sorted(available, reverse=True)
    # Assume available is reverse sorted at each loop
    while len(available) is not 0:
        step = available.pop()
        string += step
        for stepi in rev[step]:
            req[stepi].remove(step)
            if len(req[stepi]) is 0:
                available.append(stepi)
                available = sorted(available, reverse=True)
    return string

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    req = defaultdict(set)
    rev = defaultdict(set)

    r = re.compile('Step (?P<x>\w+) must be finished before step (?P<y>\w+) can begin.')
    with open(args.input) as f:
        for l in f:
            m = r.search(l)
            req[m.group('y')].add(m.group('x'))
            rev[m.group('x')].add(m.group('y'))

    print('P1: ', p1(req, rev))
