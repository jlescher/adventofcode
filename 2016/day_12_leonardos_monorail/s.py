#!/usr/bin/env python3


import argparse

registers = {}


class Proc:

    def __init__(self, prog, **kwargs):
        self.prog = prog
        self.pc = 0
        self.registers = kwargs.copy()

    def get_val(self, x):
        try: 
            return int(x)
        except ValueError:
            return self.registers.setdefault(x, 0)

    def cpy(self, x, y):
        self.registers[y] = self.get_val(x)
        self.pc += 1

    def inc(self, x):
        self.registers[x] = self.get_val(x) + 1
        self.pc += 1

    def dec(self, x):
        self.registers[x] = self.get_val(x) - 1
        self.pc += 1

    def jnz(self, x, y):
        if self.get_val(x) is not 0:
            self.pc += self.get_val(y)
        else:
            self.pc += 1

    def run(self):
        while 0 <= self.pc < len(prog):
            getattr(self, self.prog[self.pc][0])(*self.prog[self.pc][1:])
        return self.get_val('a')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = f.readlines()

    prog = [ x.strip().split() for x in prog ]

    print('P1:', Proc(prog).run())
    print('P2:', Proc(prog, c=1).run())
