import math

# Y=sum of 1000 rv's Xi, each Xi ~ Poisson(999000).
lamb = 999000
n = 1000

# Apparently the sum of Poisson variables is also a Poisson distribution, with
# lambda = sum of the lambdas. Probability mass function of Poisson variable Y:
#
#   P{Y=y} = (e^-n*lambda)(lambda^y)/(y!)
#
# Exercise 3.17 asks P{Y<999000}, the sum from y=0 to 999000-1 of P{Y=y}.

e = math.exp(1)

# Python isn't precise enough for this, e^-n*lambda is 0.0.
p = sum(
    (math.pow(e, -n * lamb)) * (math.pow(lamb, y)) / (math.factorial(y))
    for y in range(999000 - 1)
)

print(p)
