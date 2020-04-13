#!/usr/bin/env python3

import argparse
import re
from collections import defaultdict
import pudb


def get_ORE(n):
    needed = defaultdict(lambda: 0) # elements that are required
    stock = defaultdict(lambda:0)   # keep track of the over-production

    # Init
    needed['FUEL'] = n

    ORE = 0
    while needed:
        elem, unit = needed.popitem()

        # Increment ORE counter if needed
        if elem == 'ORE':
            ORE += unit
            continue

        # See if we have the element in stock
        s = stock.get(elem, 0)
        stock[elem] -= min(unit, s)
        unit -= min(unit, s)

        # Produce at least "unit" units of elements
        if unit:
            coeff = formulas[elem]['out']
            mul = unit // coeff
            if unit % coeff: # Over produce
                mul += 1
                stock[elem] = (coeff * mul) - unit
            for e, c in formulas[elem]['in']:
                needed[e] += mul*c
    return ORE

def part1(formulas):
    return get_ORE(1)

def part2(formulas):
    hold = 1000000000000
    low = 1
    high = 1000000000000
    assert get_ORE(low) < hold
    assert get_ORE(high) > hold
    while high - low > 1:
        mid = (high + low) // 2
        if get_ORE(mid) < hold:
            low = mid
        else:
            high = mid
    return low

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    # Dictionnary index by elements
    formulas = {}

    with open(args.input) as f:
        for line in f:
            nums = re.findall(r'\d+', line)
            elems = re.findall(r'[A-Z]+', line)
            formulas.update({
                elems[-1]:
                {
                    'out': int(nums[-1]),
                    'in': tuple( (x, int(y)) for x, y in zip(elems[0:-1], nums[0:-1]))
                    }
                })

    print('part1: {}'.format(part1(formulas)))
    print('part2: {}'.format(part2(formulas)))
