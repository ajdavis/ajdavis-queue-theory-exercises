# Two people show up at a random time in an hour. First to arrive waits up to
# 15 minutes for second. Probability they meet?
import math
import random

n = 10000000
meetings = 0
for _ in range(n):
    x = random.random() * 60
    y = random.random() * 60
    if math.fabs(x - y) < 15:
        meetings += 1

p = meetings / n
print(p)
