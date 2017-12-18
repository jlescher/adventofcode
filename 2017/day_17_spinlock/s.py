#!/usr/bin/env python3

from collections import deque

SPIN = 304
# Consider that the current value if the last element of the buffer
buf = deque([])
for i in range(50000000):
    buf.rotate(-SPIN)
    buf.append(i)
print(buf[buf.index(0) + 1])

