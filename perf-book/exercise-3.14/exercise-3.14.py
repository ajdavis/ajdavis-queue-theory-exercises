from numpy.random import exponential, uniform


samples = 100000000
positives = 0
for _ in range(samples):
    if exponential(5) + uniform(1, 3) <= 7:
        positives += 1

# About .6298
print(f"P{{X+Y<=7}}: {float(positives) / samples}")
