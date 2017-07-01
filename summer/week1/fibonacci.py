#!/usr/bin/env python


def fib1(n):
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print a,
        a, b = b, a+b

def fib2(n):
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print a,
        a, b = b, a+b

print "PyCharm changes whitespace...use Sublime and see source code: it may seem hidden, " \
      "but what is the only diff between 'fib1' and 'fib2' (besides 1 vs. 2)?"

print 'Ken: use Sublime show the "whitespace" difference between fib1 and fib2'