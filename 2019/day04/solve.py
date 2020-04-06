#!/usr/bin/env python3

import math
from itertools import tee
import re

LOW=234208
HIGH=765869

part1_cnt = 0
part2_cnt = 0
for n in range(LOW, HIGH+1):
    # 6 digits
    if int(math.log10(n))+1 != 6:
        continue

    # 2 consecutive digits
    str_n = str(n)
    if not re.search(r'(\d)\1', str_n):
        continue

    # Never decrease
    if list(str_n) != list(sorted(str_n)):
        continue

    part1_cnt += 1

    # No 3 times the same digit
    conseq_digits = re.findall(r'((\d)\2+)', str_n)
    for conseq,_ in conseq_digits:
        if len(conseq) == 2:
            part2_cnt += 1
            break

print('part1: {}'.format(part1_cnt))
print('part1: {}'.format(part2_cnt))
