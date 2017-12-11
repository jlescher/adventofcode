#!/usr/bin/env python3


with open('input') as f:
    stream = f.readline().rstrip()
    inside_garbage = False
    nest_level = 0
    score = 0
    removed_garbage = 0
    pending_question_mark = False
    for c in stream:
        if pending_question_mark:
            pending_question_mark = False
            continue
        if c == '!':
            pending_question_mark = True
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
    print('score: {}'.format(score))
    print('garbage: {}'.format(removed_garbage))
