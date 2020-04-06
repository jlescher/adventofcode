#!/usr/bin/env python3

with open('input') as f:
    banks = list(map(int, f.readline().split()))

    redistribution_cnt = 0
    states = []
    while True:
        # Has state been reached before?
        state = tuple(banks)
        if state in states:
            print('P1 :', redistribution_cnt)
            print('P2 :', redistribution_cnt - states.index(state))
            break
        else:
            states.append(state)
        # Distribute
        redistribution_cnt += 1
        m = max(banks)
        ix = banks.index(m)
        banks[ix] = 0
        inc = m // len(banks)
        mod = m % len(banks)
        for i in range(mod):
            banks[(ix+1+i)%len(banks)] += inc+1
        if inc != 0:
            for i in range(len(banks) - mod):
                banks[(ix++1+mod+i)%len(banks)] += inc
        if redistribution_cnt > 10000:
            break

