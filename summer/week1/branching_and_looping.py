#!/usr/bin/env python

from fractions import Fraction

class PFrac(Fraction):
    
    def __init__(self):
        super(PFrac, self).__init__()
#-------------------------------------------------------------------------------


# for loop that iterates over list of dog names
prefix = 'Mo'
suffix = 'y'
dogs = ['Roxy', 'Moe', 'Dirt']
print '\nFirst, a for loop...'
for dog in dogs:
    if dog.startswith(prefix): # BRANCHING STARTS HERE
        print 'The dog named %s starts with %s.' % (dog, prefix)
    elif dog.endswith(suffix):
        print 'The dog named %s ends with %s.' % (dog, suffix)
    else:
        print 'The dog named %s does not match our prefix or our suffix.' % dog

# -------------------------------------------------------------------------------

# while loop that iterates over list of dog names
print '\nNow a while loop...'
while dogs:
    print 'There are %d dogs remaining and current one is %s.' % (len(dogs), dogs[0])
    del dogs[0] # remove first element in list each time through the loop
