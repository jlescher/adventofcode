#!/usr/bin/env python3


import argparse
import re
import string
from collections import Counter
from collections import deque

class Room:

    def __init__(self, string):
        match = re.match('(?P<name>[a-z-]*)(?P<sector>\d*)\[(?P<checksum>\w*)\]', string)
        self.name = match.group('name')
        self.sector = int(match.group('sector'))
        self.checksum = match.group('checksum')

    def __str__(self):
        return 'name={}, sector={}, checksum={}'.format(self.name, self.sector, self.checksum)

    def is_real(self):
        char_freq = Counter(self.name.replace('-', '')).most_common()
        char_freq = sorted(sorted(char_freq, key=lambda x: x[0]), key=lambda x:x[1], reverse=True)[0:5]
        char_freq = ''.join(x[0] for x in char_freq)
        return char_freq == self.checksum

    def decrypt_name(self):
        shift = deque(string.ascii_lowercase)
        shift.rotate(-self.sector) # modulo 26 should be optimize in the deque implementation
        dec = ''
        for c in self.name:
            if c is '-':
                char = ' '
            else:
                char = shift[string.ascii_lowercase.index(c)]
            dec += char
        return dec


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        rooms = []
        for l in f:
            rooms.append(Room(l.rstrip()))

        cnt = 0
        for r in rooms:
            if r.is_real():
                cnt += r.sector
        print('P1:', cnt)

        for r in rooms:
            dec = r.decrypt_name()
            if 'north' in dec or 'pole' in dec:
                print('P2:', r.sector)

