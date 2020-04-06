#!/usr/bin/env python3


with open('input') as f:
    stream = f.readline().rstrip()
    inside_garbage = False
    nest_level = 0
    score = 0
    removed_garbage = 0
    pending_exclamation_mark = False
    for c in stream:
        if pending_exclamation_mark:
            pending_exclamation_mark = False
            continue
        if c == '!':
            pending_exclamation_mark = True
            continue
        if inside_garbage:
            if c == '>':
                inside_garbage = False
                continue
            else:
                removed_garbage += 1
                continue
        else:
            if c == '<':
                inside_garbage = True
            elif c == '{':
                nest_level += 1
            elif c == '}':
                score += nest_level
                nest_level -= 1
                continue
            else:
                continue
    assert(nest_level == 0)
    print('P1:', score)
    print('P2:', removed_garbage)
