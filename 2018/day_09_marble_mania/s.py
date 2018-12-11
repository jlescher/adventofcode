#!/usr/bin/env python3

from collections import deque
from collections import defaultdict

def p1(players, marbble):
    # current marbble is at the beginning of the deque
    score = defaultdict(int)
    q = deque([0])
    cur_p = 1  # Current player
    cur_23 = 1 # Current modulo23 marbble value
    for m in range(1, marbble + 1):
        if cur_23 != 23:
            q.rotate(-2)
            q.appendleft(m)
        else:
            score[cur_p] += m
            q.rotate(7)
            score[cur_p] += q.popleft()
        cur_23 += 1
        cur_p  += 1
        if cur_p == players:
            cur_p = 0
        if cur_23 == 24:
            cur_23 = 1
    return max(score.values())


if __name__ == '__main__':
    print('P1: ', p1(468, 71843))
    print('P2: ', p1(468, 100*71843))

