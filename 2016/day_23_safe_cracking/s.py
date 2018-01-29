#!/usr/bin/env python3


import argparse
from inspect import signature

import importlib.util
spec = importlib.util.spec_from_file_location("j12_proc", "../j12_leonardos_monorail/s.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

class Proc_toggle(foo.Proc):
    def __init__(self, prog, init_val):
        super().__init__(prog)
        self.registers['a'] = init_val

    def mul(self, x, y, z):
        self.registers[x] = self.get_val(y) * self.get_val(z)
        self.pc += 1
    
    def nop(self):
        self.pc += 1

    def tgl(self, x):
        toggle_ix = self.pc + self.get_val(x)
        if 0 <= toggle_ix < len(self.prog): # toggle in program
            func_name = self.prog[toggle_ix][0]
            func = getattr(self, func_name)
            if func_name == 'inc':
                self.prog[toggle_ix][0] = 'dec'
            elif len(signature(func).parameters) == 1: # 1 argument
                self.prog[toggle_ix][0] = 'inc'
            elif func_name == 'jnz':
                self.prog[toggle_ix][0] = 'cpy'
            elif len(signature(func).parameters) == 2: # 2 argument
                self.prog[toggle_ix][0] = 'jnz'
            else:
                raise(Exception())
        self.pc += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input_mul', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        prog = f.readlines()

    print('P1:', Proc_toggle(prog, 7).run())
    print('P2:', Proc_toggle(prog, 12).run())
