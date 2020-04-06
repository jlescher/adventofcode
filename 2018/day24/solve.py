#!/usr/bin/env python3

import argparse
import re
import pdb
import logging
from copy import deepcopy
from itertools import count

logging.basicConfig(level=logging.WARNING)

class Group:
    def __init__(self, num, is_immune, units, hitpoint, attack_damage, attack_type, weakness, immunities, initiative):
        self.num           =  num       # For debug purposes
        self.is_immune     =  is_immune
        self.units         =  units
        self.hitpoint      =  hitpoint
        self.attack_damage =  attack_damage
        self.attack_type   =  attack_type
        self.weakness      =  weakness
        self.immunities    =  immunities
        self.initiative    =  initiative
    
    def get_effective_power(self):
        return self.units * self.attack_damage

    def get_deal_damage(self, other_group):
        if self.attack_type in other_group.immunities:
            return 0
        if self.attack_type in other_group.weakness:
            return 2*self.get_effective_power()
        return self.get_effective_power()

    def log_get_deal_damage(self, other_group):
        damage = self.get_deal_damage(other_group)
        #logging.debug('{} group {} would deal defending group {} {} damage'.format('Immune System' if self.is_immune else 'Infection', self.num, other_group.num, damage))
        return damage

    def attack(self):
        if self.target:
            kills = min (self.target.units, self.get_deal_damage(self.target) // self.target.hitpoint)
            if kills > 0:
                logging.debug('{} group {} attacks defending group {} killing {} units'.format('Immune System' if self.is_immune else 'Infection', self.num, self.target.num, kills))
                self.target.units -= kills

    def select_target(self, targets):
        targets.sort(key = lambda x: (self.log_get_deal_damage(x), x.get_effective_power(), x.initiative), reverse = True)
        if targets and self.get_deal_damage(targets[0]) > 0:
            self.target = targets.pop(0)
        else:
            self.target = None

    def __str__(self):
        return '{} group {:2d} units:{:4d} hitpoint:{:5d} attack_damage:{:4d} effective_power:{:6d} initiative:{} attack_type:{} weakness:{} immunities:{}'.format('Immune System' if self.is_immune else 'Infection', self.num, self.units, self.hitpoint, self.attack_damage, self.get_effective_power(), self.initiative, self.attack_type, sorted(self.weakness), sorted(self.immunities))


def select_target(attackers, defenders):
    targets = defenders[:]
    for g in sorted(attackers, key = lambda x: (x.get_effective_power(), x.initiative), reverse = True):
        g.select_target(targets)

def attack(groups):
    for g in sorted(groups, key = lambda x: x.initiative, reverse = True):
        g.attack()


def run(groups, boost):
    logging.debug('run with boost:{}'.format(boost))

    # Don't modify groups
    groups = deepcopy(groups)

    # Init
    immune    = [ g for g in groups if g.is_immune ]
    infection = [ g for g in groups if not g.is_immune ]

    for g in immune:
        g.attack_damage += boost

    # Keep fighting while the two armies are alive and the number of units changes
    prev_units = 0
    cur_units  = sum ( [ g.units for g in groups ] )

    while immune and infection and prev_units != cur_units:

        # Log
        logging.debug('='*80)
        for g in immune:
            logging.debug(g)
        for g in infection:
            logging.debug(g)
        logging.debug('')

        select_target(infection, immune)
        select_target(immune, infection)

        attack(groups)

        # Remove the dead bodies
        groups    = [ g for g in groups    if g.units > 0 ]
        immune    = [ g for g in immune    if g.units > 0 ]
        infection = [ g for g in infection if g.units > 0 ]

        # Update while-condition
        prev_units = cur_units
        cur_units  = sum([ g.units for g in groups ])

    return not infection, cur_units


def part1(groups):
    return run(groups, 0)[1]


def part2(groups):
    for boost in count(1):
        end, units = run(groups, boost)
        if end:
            return units


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    args = parser.parse_args()

    with open(args.input) as f:
        groups = []
        is_immune = None
        for l in f:
            l = l.rstrip()
            if not l:
                continue
            elif 'Immune System' in l:
                is_immune = True
                num = 0
            elif 'Infection' in l:
                is_immune = False
                num = 0
            else:
                num += 1
                units, hitpoint, attack_damage, initiative = map(int, re.findall(r'\d+', l))
                attack_type = re.search(r'\d+\s+(\w+)\s+damage', l).groups()[0]
                try:
                    weakness = set(re.search(r'weak to ([^;)]+)', l).groups()[0].split(', '))
                except:
                    weakness = set()
                try:
                    immunities = set(re.search(r'immune to ([^;)]+)', l).groups()[0].split(', '))
                except:
                    immunities = set()
                groups.append(Group(num, is_immune, units, hitpoint, attack_damage, attack_type, weakness, immunities, initiative))
    print('part1: {}'.format(part1(groups)))
    print('part2: {}'.format(part2(groups)))
