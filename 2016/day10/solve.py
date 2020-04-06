#!/usr/bin/env python3


import argparse


class Container:
    def __init__(self, num):
        self.vals = []
        self.num = num

    def set_val(self, x):
        self.vals.append(x)
        self.vals = sorted(self.vals)

    def __str__(self):
        return 'num:{} vals:{}'.format(self.num, self.vals)


class Bot(Container):
    def __init__(self, num):
        super().__init__(num)
        self.low = None
        self.high = None

    def set_val(self, x):
        if len(self.vals) >= 2:
            raise(Exception('Bot is full'))
        else:
            self.vals.append(x)
            self.vals = sorted(self.vals)
            if self.vals == [17, 61]:
                print('P1:', self.num)
            self.dispatch()

    def set_rule(self, low, high):
        self.low = low
        self.high = high

    def dispatch(self):
        if len(self.vals) < 2:
            pass
        else:
            self.high.set_val(self.vals.pop())
            self.low.set_val(self.vals.pop())

    def __str__(self):
        return 'num:{} vals:{}, low:{}, high:{}'.format(self.num, self.vals, self.low.num, self.high.num)


def get_bot_or_output(s, num):
    if s == 'bot':
        return bots.setdefault(num, Bot(num))
    elif s == 'output':
        return outputs.setdefault(num, Container(num))
    else:
        raise(Exception('Not sure what you mean'))


def parse(s):
    if s[0] == 'value':
        e = get_bot_or_output(l[4], int(l[5]))
        e.set_val(int(l[1]))
    else:
        low_e  = get_bot_or_output(l[5], int(l[6]))
        high_e = get_bot_or_output(l[10], int(l[11]))
        e      = get_bot_or_output(l[0], int(l[1]))
        e.set_rule(low_e, high_e)


# Dictionnaries of bots and outputs
bots = {}
outputs = {}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        ins = f.readlines()
        ins = sorted(ins) # Sort so that low and high are defined before dispatching
        ins = [ x.rstrip().split() for x in ins ]

    for l in ins:
        parse(l)

    mul = 1
    for i in [0, 1, 2]:
        mul *= outputs[i].vals.pop()
    print('P2:', mul)
        
