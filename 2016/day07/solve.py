#!/usr/bin/env python3


import argparse
import re


class Address:
    def __init__(self, string):
        self.bracket = re.findall(r'\[([^\]]*)\]', string)
        self.nobracket = re.findall(r'([^\[\]]+)(?:\[[^\]]*\])?', string)

    def __str__(self):
        return 'bracket:{} nobracket:{}'.format(self.bracket, self.nobracket)
    
    def support_tls(self):
        m = re.compile(r'(.)(?!\1)(.)\2\1')
        for e in self.bracket:
            if m.search(e):
                return False
        for e in self.nobracket:
            if m.search(e):
                return True
        return False

    def support_ssl(self):
        m = re.compile(r'(?=(.)(?!\1)(.)\1)')
        nobracket_set = { e for x in self.nobracket for e in m.findall(x)}

        m = re.compile(r'(?=(.)(?!\1)(.)\1)')
        bracket_set = { tuple(reversed(e)) for x in self.bracket for e in m.findall(x)}

        return not bracket_set.isdisjoint(nobracket_set)

        
if __name__ == '__main__':

    assert(Address('abba[mnop]qrst').support_tls())
    assert(not Address('abcd[bddb]xyyx').support_tls())
    assert(not Address('aaaa[qwer]tyui').support_tls())
    assert(Address('ioxxoj[asdfgh]zxcvbn').support_tls())

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        addresses = [ Address(x.rstrip()) for x in f ]

    print('P1:', len(list(filter(Address.support_tls, addresses))))
    print('P2:', len(list(filter(Address.support_ssl, addresses))))
