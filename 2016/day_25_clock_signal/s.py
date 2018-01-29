#!/usr/bin/env python3

import argparse
from inspect import signature
import importlib.util
spec = importlib.util.spec_from_file_location("j12_proc", "../j12_leonardos_monorail/s.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

class Proc_out(foo.Proc):
    def __init__(self, prog, init_val):
        super().__init__(prog)
        self.registers['a'] = init_val
        self.string = ''

    def out(self, x):
        self.string += self.get_val(x)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', default='input', type=str)
    args = parser.parse_args()

