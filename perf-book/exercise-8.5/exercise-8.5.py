import random


def trial():
    x, y, i = 0, 0, 0
    while True:
        if random.randint(0, 1) == 0:
            # Move to a random new x, can't stay at the same x.
            new_x = random.randint(0, 6)
            x = new_x + 1 if new_x >= x else new_x
        else:
            # Move to a random new y, can't stay at the same y.
            new_y = random.randint(0, 6)
            y = new_y + 1 if new_y >= y else new_y

        if x == y == 7:
            return i

        i += 1


n = int(1e6)
T_sum, T_squared_sum = 0, 0
for _ in range(n):
    T = trial()
    T_sum += T
    T_squared_sum += T * T

expected_value = T_sum / n
variance = T_squared_sum / n - expected_value * expected_value
# Approximately 69.03 and 4632.9.
print(f"E[T] = {expected_value}, Var(T) = {variance}")
