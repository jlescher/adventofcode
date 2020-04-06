#!/usr/bin/env python3

from pprint import pprint
import argparse
import numpy as np
import re

regex_dict = {
        # Match line
        'guard' : re.compile(r'^\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<min>\d+)\] Guard #(?P<id>\d+) begins shift$'),
        'sleep' : re.compile(r'^\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<min>\d+)\] falls asleep$'),
        'wake'  : re.compile(r'^\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<min>\d+)\] wakes up$'),
        }

def parse_line(line):
    for key, regex in regex_dict.items():
        match = regex.search(line)
        if match:
            return key, match
    # If there are no matches.
    return None, None

def parse_file(infile):
    with open(infile) as f:
        raw_shifts = f.read().splitlines()

    raw_shifts.sort()
    shifts = {}
    awake = True # Track wether the current gard is sleeping or not

    for s in raw_shifts:
        key, match = parse_line(s)

        if key == 'guard':
            # End of shift of the previous guard.
            if not awake:
                shifts[cur_id][start:60] += 1

            # New guard info.
            cur_id = int(match.group('id'))
            awake = True
            if cur_id not in shifts.keys():
                shifts[cur_id] = np.zeros(60)

        if key == 'sleep':
            # Sanity check
            if not awake:
                raise() 
            awake = False
            start = int(match.group('min'))

        if key == 'wake':
            # Sanity check
            if awake:
                raise() 
            awake = True
            shifts[cur_id][start: int(match.group('min'))] += 1

    # End of shift of the previous guard.
    if not awake:
        shifts[cur_id][start:60] += 1

    return shifts

def p1(shifts):
    id_max = max(shifts, key = lambda key: shifts[key].sum())
    return int(id_max * np.argmax(shifts[id_max]))

def p2(shifts):
    asleep = [ (id, np.max(shifts[id]), np.argmax(shifts[id])) for id in shifts ]
    e = max(asleep, key=lambda x: x[1])
    return e[0] * e[2]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    shifts = parse_file(args.input)
    print('P1: ', p1(shifts))
    print('P2: ', p2(shifts))
