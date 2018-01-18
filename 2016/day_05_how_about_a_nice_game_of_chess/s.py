#!/usr/bin/env python3

import hashlib

KEY = 'ugkcyxxp'

def gen(key, p):
    '''
    Generator that returns the successive numbers of the password
    '''
    start = 0
    while True:
        h = hashlib.md5((key+str(start)).encode()).hexdigest()
        if h[0:5] == '00000':
            if p == 1:
                yield h[5]
            else:
                yield h
        start += 1

# P1
password = ''
for _, c in zip(range(8), gen(KEY, 1)):
    password += c
print('P1:', password)

# P2
password = [ '-' ] * 8 
gen = iter(gen(KEY, 2))
while  '-' in password:
    h = next(gen)
    if h[5] in '01234567':
        ix = int(h[5])
        if password[ix] == '-': 
            password[ix] = h[6]
print('P2:', ''.join(password))
