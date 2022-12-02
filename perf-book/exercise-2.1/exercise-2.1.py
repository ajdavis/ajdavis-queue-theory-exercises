# Exercise 2.1 of Performance Modeling and Design of Computer Systems.
# See Figure 2.3.
#
# Run this like "python3 exercise-2.1.py 5.1999", where 5.1999 is a possible
# value of r1, i.e. a possible answer to Exercise 2.1. If 5.1999 is a stable
# value of r1 then this script exits with code 0, otherwise it fails. Try a few
# values to find the max allowable.

import sys
from collections import defaultdict

# Each server's service rate.
mu = 10.0
servers = {1, 2, 3}
# Outside arrival rates for servers 1, 2, and 3.
# The question: what's the max value of r1?
r = {1: float(sys.argv[1]), 2: 1., 3: 1.}
# Probability a packet travels from server 1 to 2.
p12 = 0.8
# Probability a packet travels from server 2 to 3, or 1 to 3.
p23 = p13 = 0.2

# Number of jobs in each queue, default 0.
q = defaultdict(float)


def tick():
    """A unit of time passes."""
    global q

    for s in servers:
        # Outside arrivals join each server's queue.
        q[s] += r[s]

    if q[1] > 0:
        # Do task(s) of size up to mu in this tick of the simulation.
        size = min(q[1], mu)
        q[1] -= size
        q[2] += size * p12
        q[3] += size * p13

    if q[2] > 0:
        size = min(q[2], mu)
        q[2] -= size
        q[3] += size * p23

    if q[3] > 0:
        size = min(q[3], mu)
        q[3] -= size
        # We know p31 == 1.0, tasks always go from server 3 to server 1.
        q[1] += size


def stable(t):
    for s, n in q.items():
        if n > 100:
            print(f"Queue length for {s} is {n} at time {t}, r1={r[1]}")
            return False

    return True


def main():
    for t in range(100000):
        if stable(t):
            tick()
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
