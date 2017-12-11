#!/usr/bin/env python3

# What are the pythonic solutions for a circular buffer?
# I have only thought of:
#   - regular lists ? -> used with `mylist[index % len(mylist)]`
#   - collections.deque -> supports rotate but does not support slicing (unless using itertools.islice)

BUF_LEN = 256
END_LIST = [17, 31, 73, 47, 23]

def left_rotate(n, l):
    n = n % len(l)
    return l[n:] + l[:n]

def right_rotate(n, l):
    return left_rotate(-n, l)

with open('input', mode='rb') as f:
    circular_buffer = [ x for x in range(BUF_LEN) ]
    skip_size = 0
    left_shift = 0
    # Not sure what am I doing but it seems to do the job
    lengths = list(map(ord, map(chr, f.read().rstrip()))) + END_LIST
    for _ in range(64):
        for length in lengths:
            circular_buffer[0:length] = circular_buffer[0:length][::-1]
            circular_buffer = left_rotate(length + skip_size, circular_buffer)
            left_shift += length + skip_size
            skip_size += 1
    circular_buffer = right_rotate(left_shift, circular_buffer)
    
    dense_hash = []
    for i in range(0, len(circular_buffer), 16):
        xor = 0
        for j in range(i, i+16):
            xor = xor ^ circular_buffer[j]
        dense_hash.append(xor)
    assert(len(dense_hash) == 16 )

    a = ''
    for e in  dense_hash:
        a += '{:02x}'.format(e)
    print(a)
