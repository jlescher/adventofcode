#!/usr/bin/env python3

from collections import defaultdict
from pprint import pprint
import copy
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
    req = copy.deepcopy(req)
    rev = copy.deepcopy(rev)
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

def p2(req, rev):
    time = 0
    # Find all steps that do not require a req.
    string = ''
    # A worker has format [ <time before end of step> , <step> ]
    workers =  [ [0, None] for _ in range(5) ]
    available = [ *set(rev).difference(set(req)) ]
    available = sorted(available, reverse=True)
    # Assume available is reverse sorted at each loop.
    while True:
        # Assign as many steps as possible.
        for w in workers:
            if w[1] is None:
                try:
                    e = available.pop()
                    w[0] = 60 + ord(e) - ord('A') + 1
                    w[1] = e
                except:
                    pass
        # Poor man's timer: fast-forward time.
        try:
            m = min([ w[0] for w in workers if w[1] is not None])
        except:
            # All workers are idle and there are no available steps.
            break
        time += m
        workers = list(map(lambda x: [x[0] - m, x[1]], workers))

        # Update the available steps.
        tmp_string = '' # To re-order is several steps finish at the same time.
        for w in workers:
            if w[0] is 0 and w[1] is not None:
                e = w[1]
                w[1] = None
                tmp_string += e
                for stepi in rev[e]:
                    req[stepi].remove(e)
                    if len(req[stepi]) is 0:
                        available.append(stepi)
        available = sorted(available, reverse=True)
        string += ''.join(sorted(tmp_string))
    return time

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
    print('P2: ', p2(req, rev))
