# Exercise 2.1 of Performance Modeling and Design of Computer Systems.
# See Figure 2.3.

import sys
from collections import defaultdict
from random import random

# Each server's service rate.
mu = 10
servers = {1, 2, 3}
# Outside arrival rates for servers 1, 2, and 3.
# The question: what's the max value of r1?
r = {1: int(sys.argv[1]), 2: 1, 3: 1}
# Probability a packet travels from server 1 to 2, or 2 to out.
p12 = p2out = 0.8
# Probability a packet travels from server 1 out.
p1out = 0.0
# Probability a packet travels from server 2 to 3, or 1 to 3.
p23 = p13 = 0.2
# Probability a packet travels from server 3 to 1.
p31 = 1.0

# Number of jobs in each queue, default 0.
q = defaultdict(int)

assert type(r[1]) == int, "Not ready for reals yet"
assert p12 + p13 + p1out == 1.0
assert p23 + p2out == 1.0
assert p31 == 1.0


def tick():
    """A unit of time passes."""
    global q

    for s in servers:
        # Outside arrivals join each server's queue.
        q[s] += r[s]

    for _ in range(mu):
        q_next = q.copy()
        if q[1]:
            sample = random()
            q_next[1] -= 1
            if sample <= p12:
                q_next[2] += 1
            elif sample <= (p12 + p13):
                q_next[3] += 1
            else:
                assert False

        if q[2]:
            sample = random()
            q_next[2] -= 1
            if sample <= p23:
                q_next[3] += 1
            elif sample <= p23 + p2out:
                # Out.
                pass
            else:
                assert False

        if q[3]:
            sample = random()
            q_next[3] -= 1
            if sample <= p31:
                q_next[1] += 1
            else:
                assert False

        q = q_next


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
