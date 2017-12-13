#!/usr/bin/env python3

def get_severity(layers):
    severity = 0
    for layer, scan_range in layers.items():
        if get_scanner_position(scan_range, layer) == 0:
            severity += scan_range * layer
    return severity

def got_caught(initial, layers):
    for layer, scan_range in layers.items():
        if get_scanner_position(scan_range, layer+initial) == 0:
            return True
    return False

def get_scanner_position(scan_range, picoseconds):
    num_pos = (scan_range - 1)  * 2
    mod = picoseconds % num_pos
    if mod < scan_range:
        return mod
    else:
        return num_pos - mod

with open('input') as f:
    layers = {}
    for l in f.readlines():
        num,  depth = map(int, l.rstrip().split(': '))
        layers[num] = depth

    delay = 0
    # It could possibly be an infinite loop
    # To be safe, we could define the upper bound as the PPCM of all the layers' number
    while got_caught(delay, layers):
        delay += 1
    print(delay)
