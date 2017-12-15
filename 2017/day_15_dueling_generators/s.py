#!/usr/bin/env python3

class Gen:
    def __init__(self, mul, init, modulo):
        self.mul = mul
        self.init = init
        self.modulo = modulo
        self.lower = 0

    def run(self):
        tmp = self.mul * self.init
        # Useless manual optmization of 'modulo 0x7fffffff'
        #
        # tmp = a  * 0x80000000 + b      with b  in [0 : 0x7ffffffff]
        # tmp = a' * 0x7fffffff + b'     with b' in [0 : 0x7fffffffe]
        # b' = b + a * 0x80000000 - a' * 0x7fffffff
        # b' = b + a + (a - a') * 0x7fffffff
        # b' % 0x7fffffff  = (b + a) % 0x7fffffff
        b = tmp & 0x7fffffff
        a = (tmp - b) >> 31
        x = a + b
        if x > 0x7fffffff:
            self.init = x - 0x7fffffff
        else:
            self.init = a + b
        self.lower = self.init & 0xffff

    def get_val(self):
        self.run()
        while (self.lower % self.modulo) != 0:
            self.run()

    def __str__(self):
        return '{:15}'.format(self.init)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.lower == other.lower

with open('input') as f:
    genA = Gen(16807, int(f.readline().split()[-1]), 4)
    genB = Gen(48271, int(f.readline().split()[-1]), 8)

match = 0
for _ in range(5000000):
    genA.get_val()
    genB.get_val()
    if genA == genB:
        match += 1
print(match)
