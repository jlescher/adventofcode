#!/usr/bin/env python3

def nodup(passphrases):
    nodup_passphrases = [ set(x) for x in passphrases ]
    cnt = 0
    for p, nodup_p in zip(passphrases, nodup_passphrases):
        if len(p) == len(nodup_p):
            cnt += 1
    return cnt


def no_anagram(passphrases):
    no_anagram_passphrases = passphrases[:]
    no_anagram_passphrases = list(map(lambda x: set(tuple(map(lambda y: tuple(sorted(y)), x))), passphrases))
    cnt = 0
    for p, no_anagram_p in zip(passphrases, no_anagram_passphrases):
        if len(p) == len(no_anagram_p):
            cnt += 1
    return cnt


with open('input') as f:
    passphrases = list(map(lambda x: x.rstrip().split(), f.readlines()))
    print('P1:', nodup(passphrases))
    print('P2:', no_anagram(passphrases))
