from random import random


def trial():
    i = 0
    cost = 0
    while True:
        i += 1
        if random() >= .5:
            # generous:
            cost += 1000
            if random() >= .95:
                # success
                return i, cost
        else:
            # cheapskate:
            cost += 50


trials = 10000000
total_dates = 0
total_cost = 0
total_cost_squared = 0
for n in range(trials):
    i, cost = trial()
    total_dates += i
    total_cost += cost
    total_cost_squared += cost * cost

# About 40 dates and $21,000.
print(f"{float(total_dates) / trials} dates, {float(total_cost) / trials} cost, {float(total_cost_squared) / trials} cost squared")
