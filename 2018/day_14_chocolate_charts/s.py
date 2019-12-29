#!/usr/bin/env python3

INPUT='110201'

def part1():
    ix0 = 0
    ix1 = 1
    recipes = [3, 7]
    int_INPUT=int(INPUT)

    while len(recipes) < int_INPUT + 10:
        digits = list(map(int, str(recipes[ix0] + recipes[ix1])))
        recipes.extend(digits)
        # Move each index
        ix0 = (ix0 + 1 + recipes[ix0]) % (len(recipes))
        ix1 = (ix1 + 1 + recipes[ix1]) % (len(recipes))

    print('part1: {}'.format(''.join(map(str, recipes[int_INPUT:int_INPUT+10]))))


def part2():
    INPUT_PATTERN = list(map(int, INPUT))
    ix0 = 0
    ix1 = 1
    recipes = [3, 7]

    while True:
        digits = list(map(int, str(recipes[ix0] + recipes[ix1])))
        recipes.extend(digits)
        # Look for INPUT in the last "len(INPUT) + 2 digits"
        if INPUT_PATTERN == recipes[-len(INPUT_PATTERN):]:
            sol = len(recipes) - len(INPUT_PATTERN)
            break
        elif INPUT_PATTERN == recipes[-len(INPUT_PATTERN)-1:-1]:
            sol = len(recipes) - len(INPUT_PATTERN) - 1
            break

        # Move each index
        ix0 = (ix0 + 1 + recipes[ix0]) % (len(recipes))
        ix1 = (ix1 + 1 + recipes[ix1]) % (len(recipes))

    print('part2: {}'.format(sol))

part1()
part2()
