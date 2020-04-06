#!/usr/bin/env python3

from pprint import pprint
import re

def display_tape(ix, tape):
    print('...', end='')
    for i in range(-3, 3):
        print('[' if i == ix else ' ', end='')
        print(1 if i in tape else 0, end='')
        print(']' if i == ix else ' ', end='')
    print(' ...', end='')
    print()

with open('input') as f:
    states = {}
    _state = f.readline()[-3:-2]
    steps = int(re.search('[0-9]+', f.readline()).group())

    for l in f:
        # Ugly but pretty robust, supports:
        # - inverting the states' paragraph
        # - shuffling the "write", "move", "continue" lines
        #
        # But it does not make sense since actions must be taken in the specified order
        m = re.match('In state (?P<state>.):', l)
        if m:
            state = m.group('state')
            states[state] = {}
        m = re.search('current value is (?P<current_value>.):', l)
        if m:
            current_value = int(m.group('current_value'))
            states[state][current_value] = {}
        m = re.search('Write the value (?P<write>.)\.', l)
        if m:
            states[state][current_value]['write'] = int(m.group('write'))
        m = re.search('Move one slot to the (?P<move>\w*)\.', l)
        if m:
            states[state][current_value]['move'] = 1 if m.group('move') == 'right' else -1
        m = re.search('Continue with state (?P<next_state>.)\.', l)
        if m:
            states[state][current_value]['next_state'] = m.group('next_state')

    # Set of indexes where value is 1 on the tape
    tape = set()
    ix = 0
    for _ in range(steps):
        cur_val = 1 if ix in tape else 0
        if states[_state][cur_val]['write'] == 1:
            tape.add(ix)
        else:
            try:
                tape.remove(ix)
            except:
                pass
        ix += states[_state][cur_val]['move']
        _state = states[_state][cur_val]['next_state']
    print(len(tape))

