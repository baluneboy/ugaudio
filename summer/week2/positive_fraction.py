#!/usr/bin/env python

from fractions import Fraction


def same_sign(a, b):
    """return True if a and b both have same sign; else False"""

    # note here that we let zero be both positive and negative
    both_pos = a >= 0 and b >= 0  # True if both positive
    both_neg = a <= 0 and b <= 0  # True if both negative

    # now return True if a & b are same sign; otherwise return False
    return both_pos or both_neg


class PositiveFraction(Fraction):
    """This class implements positive fractions.

    Both arguments (numerator, denominator) must have same sign.

    """

    def __init__(self, numerator, denominator):
        """Return a PositiveFraction object given numerator & denominator."""

        # put couple/few lines of code here that test if numerator & denominator
        # have the same sign; if not, then throw an exception


        # now we have same-signed num and den, so just initialize using super
        super(PositiveFraction, self).__init__(numerator, denominator)

    def __str__(self):
        """return informal string representation of PositiveFraction"""

        # replace the code here with what makes sense for your objectives
        s = 'this is what'
        s += '\n\twe want to see when'
        s += '\n\twe print a PositiveFraction'
        return s

def show_posfrac(n, d):
    """initialize and print a PositiveFraction
       given numerator = n and denominator = d
    """
    print "numerator   =", n
    print "denominator =", d
    pf = PositiveFraction(n, d)
    print "positive fraction =", pf
    print '- ' * 22


def simple_tests():

    # no problem here (right?)
    n1, d1 = 1, 2
    show_posfrac(n1, d1)

    # again, no problem here (right?)
    n2, d2 = -1, -2
    show_posfrac(n2, d2)

    # negative numerator
    n3, d3 = -1, 2
    show_posfrac(n3, d3)

    # negative denominator WHY IS THIS LAST TEST NOT BEING CALLED/RUN?
    n4, d4 = 1, -2
    show_posfrac(n4, d4)


if __name__ == '__main__':
    simple_tests()
