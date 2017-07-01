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

        # TODO put couple/few lines of code here to test if numerator & denominator
        # TODO have the same sign; if not, then throw an exception

        # if we get past the check & exception above, then that means we
        # now have same-signed num and den, so just initialize using super
        super(PositiveFraction, self).__init__(numerator, denominator)

    def __str__(self):
        """return informal string representation of PositiveFraction"""

        # replace the code here with what makes sense for your objectives
        s = 'this is what'
        s += '\n\twe want to see when'
        s += '\n\twe print a PositiveFraction'
        return s


def show_my_fraction(n, d):
    """initialize and show a PositiveFraction
       using n for numerator and d for denominator
    """
    print "numerator   = %3d" % n
    print "denominator = %3d" % d
    pf = PositiveFraction(n, d)
    print "positive fraction =", pf
    print '- ' * 22


def simple_tests():

    # no problem here (right?)
    num1, den1 = 1, 2
    show_my_fraction(num1, den1)

    # again, no problem here (right?)
    num2, den2 = -1, -2
    show_my_fraction(num2, den2)

    # negative numerator
    num3, den3 = -1, 2
    show_my_fraction(num3, den3)

    # negative denominator WHY IS THIS LAST TEST NOT BEING CALLED/RUN?
    num4, den4 = 1, -2
    show_my_fraction(num4, den4)


if __name__ == '__main__':
    simple_tests()
