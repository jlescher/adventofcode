#!/usr/bin/env python3

def min_max_checksum(spreadsheet):
    return sum(map(lambda x: max(x) - min(x), spreadsheet))

def divider_checksum(spreadsheet):
    cnt = 0
    for l in spreadsheet:
        for dividend in l:
            for divisor in l:
                if dividend > divisor and dividend % divisor == 0:
                    cnt += dividend // divisor
    return cnt


with open('input') as f:
    cnt = 0
    # Nasty but does the work
    spreadsheet = list(map(lambda x: list(map(int, x.rstrip().split())), f.readlines()))
    print('P1:', min_max_checksum(spreadsheet))
    print('P2:', divider_checksum(spreadsheet))
