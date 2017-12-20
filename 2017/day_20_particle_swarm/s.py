#!/usr/bin/env python3

import re
import math
import itertools
import random

# steps | acceleration | velocity | position
# ----- | ------------ | -------- | --------
# n = 0 | a            | v        | p
# n = 1 | a            | a + v    | a + v + p
# n = 2 | a            | 2a + v   | 3a + 2v + p
# n = 3 | a            | 3a + v   | 6a + 3v + p
# n = 4 | a            | 4a + v   | 10a + 4v + p
# n     | a            | na + v   | n(n+1)a/2 + nv + p
# equivalent to                   | (a/2)n² + (a/2+v)n + p


def get_abs_acc(vec):
    return sum(map(lambda x: abs(x)/2, vec[3]))


def get_abs_vel(vec):
    return sum(map(lambda x: abs(x[1]/2 + x[0]), zip(vec[2], vec[3])))


def get_abs_pos(vec):
    return sum(map(abs, vec[1]))


def get_closest(vectors):
    vectors_sorted = sorted(sorted(sorted(vectors, key=get_abs_pos), key=get_abs_vel), key=get_abs_acc)
    return vectors_sorted[0][0]


def solve_positive_integer_quadratic(a, b, c):
    '''
    Solve ax²+bx+c=0

    Caveat if a == b == c == 0: any value of x solves the equation.

    Since we return a list of solutions and we cannot enumerate infinitely we
    consider that returning infinite=True means "any x is good"
    '''
    infinite = False # Required to handle the case where a == b == c == 0
    sols = []
    if a == 0 :
        if b == 0:
            if c == 0:
                infinite = True
            else:
                pass
        else:
            sol = (-c) / b 
            sols.append(sol)
    else:
        delta = b*b - 4*a*c
        if delta < 0:
            pass
        elif delta == 0:
            sol = (-b) / (2*a)
            sols.append(sol)
        else:
            sol1 = ((-b) - math.sqrt(delta)) / (2*a)
            sol2 = ((-b) + math.sqrt(delta)) / (2*a)
            sols.append(sol1)
            sols.append(sol2)
    int_sols = [ int(x) for x in sols if x.is_integer() and x >= 0 ]
    return infinite, int_sols


def get_position_at_step_n(p, axis, time):
    return (p[3][axis]/2)*(time**2) + (p[3][axis]/2 + p[2][axis])*time + p[1][axis]


def verify_collision(p0, p1, time):
    for axis in [ 0, 1, 2 ]:
        if get_position_at_step_n(p0, axis, time) != get_position_at_step_n(p1, axis, time):
            return False
    return True


def particule_collision(p0, p1):
    '''
    Given two particules return a set of tuples (p0, p1, time) with the time of their collision

    (a0/2)n² + (a0/2+v0)n + p0 = (a1/2)n² + (a1/2+v1)n + p1
    is equivalent to:
    (a0/2)n² + (a0/2+v0)n + p0 - ((a1/2)n² + (a1/2+v1)n + p1) = 0
    (a0-a1)n² + (a0 - a1 + 2v0 - 2v1)n + 2p0 - 2p1 = 0
    '''
    collisions = []

    # Solve the quadratic equation for X axis
    for axis in [ 0, 1, 2 ]:
        infinite, times = solve_positive_integer_quadratic(
                p0[3][axis] - p1[3][axis],
                p0[3][axis] + 2*p0[2][axis] - (p1[3][axis] + 2*p1[2][axis]),
                2*p0[1][axis] - 2*p1[1][axis]
                )
        if not infinite: # Check collision
            for time in times:
                if verify_collision(p0, p1, time):
                    collisions.append((p0[0], p1[0], time))
            break
    if infinite: # Particules are exactly on the same spot
        collisions.append((p0[0], p1[0], 0)) # They collide on the first spot
    return collisions 

def get_collision_list(vec):
    # Build a list [ (p0, p1, time) ]
    #
    # Where:
    # p0 is a particule number
    # p1 is a particule number
    # time is the time of their collision
    collisions = []
    for p0, p1 in itertools.combinations(vec, 2):
        collisions.extend(particule_collision(p0, p1))
    return collisions

def swarm(vec):
    # Get the list of collisions
    collisions = get_collision_list(vec)
    collisions_sorted = sorted(collisions, key = lambda x: x[2])

    # Go through the collisions
    collided = set()
    prev_time = -1
    for p0, p1, time in collisions_sorted:
        if (prev_time == time) or ((p0 not in collided) and (p1 not in collided)):
            collided.add(p0)
            collided.add(p1)
        prev_time = time
    return len(vec) - len(collided)

if __name__ == '__main__':
    with open('input') as f:
        vectors = []
        for i, l in enumerate(f):
            regexp = re.compile('-?[0-9]+')
            tmp = list(map(int, regexp.findall(l)))
            p, v, a = (lambda x: (x[0:3], x[3:6], x[6:9]))(tmp)
            vectors.append([ i, p, v, a ])
        print('P1:', get_closest(vectors))
        # Simulating the swarm for part two is easy unless you want to be extra-careful
        # with the final condition Formally speaking, when do you decide that no
        # collsion won't ever happen? have you taken into account that some particules
        # may have the same acceleration / velocity?
        #
        # Instead lets go for the algebraic solution
        print('P2:', swarm(vectors))
