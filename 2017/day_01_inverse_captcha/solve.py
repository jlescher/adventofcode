#!/usr/bin/env python3

from collections import deque

#
# What would you recommend between:
# 1. match_next_digit() and match_halfway_around()
# 2. match_rotate_left()
#

def match_next_digit(nums):
    cnt= 0
    prev = ''
    for cur in nums + nums[0]:
        if cur == prev:
            cnt += int(cur)
        prev = cur
    return cnt
    

def match_halfway_around(nums):
    cnt = 0
    half = len(nums)//2
    for cur, half in zip(nums[:half], nums[half:]):
        if cur == half:
            cnt += 2*int(cur)
    return cnt


def match_rotate_left(nums, r):
    nums_cmp = deque(nums)
    nums_cmp.rotate(-r)
    return sum([int(x[0]) if x[0] == x[1] else 0 for x in zip(nums, nums_cmp)])


with open('input') as f:
    nums = f.readline().rstrip()
    #print('P1:', match_next_digit(nums))
    #print('P2:', match_halfway_around(nums))
    print('P1:', match_rotate_left(nums, 1))
    print('P2:', match_rotate_left(nums, len(nums)//2))
