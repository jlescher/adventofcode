#!/usr/bin/env python3

import hashlib
from pprint import pprint
import re
from collections import deque

SALT='ngcjuoqr'

def gen_hash_p1():
    i = 0
    while True:
        yield hashlib.md5((SALT+str(i)).encode()).hexdigest()
        i += 1

def gen_hash_p2():
    i = 0
    while True:
        h = SALT+str(i)
        for _ in range(2017):
            h = hashlib.md5(h.encode()).hexdigest()
        i += 1
        yield h

# Append
def p(generator):
    hashes = deque([])
    # Pre-fill hashes with 1000 values:
    gen_hash_iter = generator()
    for _, h in zip(range(1000), gen_hash_iter):
        hashes.append(h)

    # Loop and look at the condition
    regex = re.compile(r'(.)\1{2}')
    key_cnt = 0
    for h_cnt, new_h in enumerate(gen_hash_iter):
        h = hashes.popleft()
        m = regex.search(h)
        if m:
            for h in hashes:
                if m.group(1)*5 in h:
                    key_cnt += 1
                    if key_cnt == 64:
                        return h_cnt
                    break
        hashes.append(new_h)


print('P1:', p(gen_hash_p1))
print('P2:', p(gen_hash_p2))
