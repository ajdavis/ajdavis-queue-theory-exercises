import decimal
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

ctx = decimal.Context()
e = ctx.create_decimal_from_float(math.exp(1))
p = 0

# This seems excessively slow and RAM-heavy.
for y in range(999000 - 1):
    p += (ctx.power(lamb, y)) / (math.factorial(y))
    if 0 == y % 1000:
        print(y, p)

print(p)
print((ctx.power(e, -n * lamb)) * p)
