+++
title = "Nth Prime Number"
date = 2011-10-14T22:57:00
description = "An early Python exercise for finding the nth prime number."
slug = "nth-prime-number"
aliases = ["nth-prime-number/"]
draft = false
[taxonomies]
tags = ["mathematics", "python"]
[extra]
legacy_source = "nth-prime-number.rst"
+++
Python implementation for finding Nth prime number.

> Archive note: this is historical Python 2 code. The original export lost some
> indentation; it has been restored below. The filename mentions the 1000th
> prime, but the original loop computes the 10,000th.

```python
#!/usr/bin/python
# thousandPrime.py : Finds the 1000th prime number, fork of Problem Set 1 MIT 6.00
# Programmed: Saurav R Tuladhar
# Date: Oct 7, 2011

# Declare state variables
counter = 1  # Counts number of primes
idx = 1
testNum = 2 * idx + 1  # Odd numbers > 2 as candidates
primeList = [2]
isPrime = True

while counter < 10000:
    for x in primeList:
        if testNum % x == 0:
            isPrime = False
            break

    if isPrime == True:
        primeList = primeList + [testNum]
        counter = counter + 1

    # Reset variables
    isPrime = True
    idx = idx + 1
    testNum = 2 * idx + 1

print primeList[-1]
```
