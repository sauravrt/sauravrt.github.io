Nth Prime Number
################
:date: 2011-10-14 22:57
:author: sauravtuladhar
:category: Math, Python
:slug: nth-prime-number
:status: published

::

   Python implementation for finding Nth prime number

   [sourcecode language="python"]

   #!/usr/bin/python
   # thousandPrime.py : Finds the 1000th prime number, fork of Problem Set 1 MIT 6.00

   # Programmed: Saurav R Tuladhar

   # Date: Oct 7, 2011
   # Declare state variables

   counter = 1;   # Counts number of primes

   idx = 1;

   testNum = 2*idx + 1;   # Odd numbers > 2 as candidates

   primeList = [2];

   isPrime = True
   while counter < 10000:

           for x in primeList:

                   if testNum % x == 0:   # Only check for prime numbers < testNum. Based on Fundamental Theorem of Arithmetic.

                           isPrime = False

                           break
   if isPrime == True:

                   primeList = primeList + [testNum]

                   counter  = counter + 1
   # Reset variables

           isPrime = True

           idx = idx + 1

           testNum = 2*idx + 1
   print primeList[-1]

   [/sourcecode]
