#!/usr/bin/env python3


import argparse
from collections import deque

READ_UNTIL_MARKER = 0
PARSE_MARKER = 1
DECOMPRESS = 2

def decompress_p1(stream):
    dec_stream = ''
    state = deque([READ_UNTIL_MARKER, PARSE_MARKER, DECOMPRESS])
    ix = 0
    while ix < len(stream):
        if state[0] == READ_UNTIL_MARKER:
            try:
                new_ix = stream.index('(', ix)
            except ValueError:
                new_ix = len(stream)
            dec_stream += stream[ix:new_ix]
            ix = new_ix + 1
            state.rotate(-1)
        elif state[0] == PARSE_MARKER:
            new_ix = stream.index(')', ix)
            pat_len, repeat = tuple(map(int, stream[ix:new_ix].split('x')))
            ix = new_ix + 1
            state.rotate(-1)
        elif state[0] == DECOMPRESS:
            pat = stream[ix:ix+pat_len]
            dec_stream += pat*repeat
            ix += pat_len
            state.rotate(-1)
        else:
            raise(Exception('Should not land here'))
    return dec_stream

def decompress_p2(stream):
    state = deque([READ_UNTIL_MARKER, PARSE_MARKER, DECOMPRESS])
    ix = 0
    cnt = 0
    while ix < len(stream):
        if state[0] == READ_UNTIL_MARKER:
            try:
                new_ix = stream.index('(', ix)
            except ValueError:
                new_ix = len(stream)
            cnt += new_ix -ix
            ix = new_ix
            state.rotate(-1)
        elif state[0] == PARSE_MARKER:
            new_ix = stream.index(')', ix)
            pat_len, repeat = tuple(map(int, stream[ix+1:new_ix].split('x')))
            ix = new_ix + 1
            state.rotate(-1)
        elif state[0] == DECOMPRESS:
            pat = stream[ix:ix+pat_len]
            cnt += repeat * decompress_p2(pat)
            ix += pat_len
            state.rotate(-1)
        else:
            raise(Exception('Should not land here'))
    return cnt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        stream = f.readline().rstrip()

    print('P1:', len(decompress_p1(stream)))

    # Check that we are not doing stupid stuff
    assert(decompress_p2('(3x3)XYZ') == 9)
    assert(decompress_p2('X(8x2)(3x3)ABCY') == 20)
    assert(decompress_p2('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920)
    assert(decompress_p2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445)
    print('P2:', decompress_p2(stream))

        



