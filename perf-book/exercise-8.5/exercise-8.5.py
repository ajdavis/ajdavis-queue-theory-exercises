import random


def trial():
    x, y, i = 0, 0, 0
    while True:
        if random.randint(0, 1) == 0:
            x = random.randint(0, 7)
        else:
            y = random.randint(0, 7)

        if x == y == 7:
            return i

        i += 1


n = int(1e5)
trial_sum, trial_squared_sum = 0, 0
for _ in range(n):
    T = trial()
    trial_sum += T
    trial_squared_sum += T * T

expected_value = trial_sum / n
variance = trial_squared_sum / n - expected_value * expected_value
# Approximately 78.7 and 6013.
print(f"E[T] = {expected_value}, Var(T) = {variance}")
