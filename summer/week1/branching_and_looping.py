#!/usr/bin/env python

# This module (this file) demonstrates 2 fundamental concepts in programming:
# 1. branching (test or compare something to decide what to do next)
# 2. looping (iterating) to repeat a block of (indented lines) steps


# for convenience, let's define a function to call as needed
def show_my_comparison(a, b):
    """compare 2 values and print a summary string"""
    # a branch to compare values and print something based on that comparison
    # TODO Zack explain here how we have exhausted all possibilities in comparison?
    if a > b:
        print 'a = %.3f, and that is bigger than b, which is %.1f' % (a, b)
    elif a == b:
        print 'huh, the areas are equal, both = %.2f' % a
    else:
        # TODO Ken explain double quotes as string delimiters needed for getting c'mon in there
        print "c'mon now, b = %.1f, which is bigger than a = %.1f" % (b, a)

# BRANCHING ------------------------------------------------------------------------------- #

# define some variables (2 floats) to work with for comparison
x = 45.0  # notice units in variable name
y = 35.0  # there are probably libraries for units that get incorporated in with the value

# TODO Zack without running program yet, can you trace steps to explain what we would expect output from next line call?
show_my_comparison(x, y)

# TODO Zack the next line calls same function with same 2 arguments (inputs), so why is the result printed different?
show_my_comparison(y, x)

# TODO Ken explain how the next line is an assignment not an algebraic formula (eval RHS, then assign that to LHS)
x = x - 10.99

# TODO Zack read off from the program output the line that corresponds to this next call -- does the match look correct?
show_my_comparison(x, y)


# LOOPING ------------------------------------------------------------------------------- #

# a "for loop" that iterates over list of dog names (and uses branching too)
# TODO Zack given we may not know what is in "dogs" list, can you explain why we probably cannot do exhaustive compare?
dogs = ['Roxy', 'Moe', 'Diggity', 'Dirt']
for dog in dogs:
    if 'o' in dog:
        print 'The dog named %s has at least one "o" in its name.' % dog
    elif dog.endswith('t'):
        print 'The dog named %s ends with a "t".' % dog
    else:
        print 'The dog named %s does not match any of our comparisons.' % dog
