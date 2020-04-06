#!/usr/bin/env python3


import argparse

def get_min_ip(ranges):
    min_ip = 0
    for r in sorted(ranges):
        if r[0] > min_ip:
            return min_ip
        else:
            min_ip = r[1]+1 if r[1] > min_ip else min_ip 
    return min_ip

def get_num_ips(ranges):
    cnt = 0
    ip = 0
    for r in sorted(ranges):
        if r[0] > ip:
            cnt += r[0] - ip
        ip = r[1]+1 if r[1]+1 > ip else ip
    return cnt + (4294967295 - ip + 1)

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        ranges = [ tuple(map(int, l.rstrip().split('-'))) for l in f ]

    print('P1:', get_min_ip(ranges))
    print('P2:', get_num_ips(ranges))
