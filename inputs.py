#!/usr/bin/env python

"""ugaudio

For important considerations and disclaimers, read the readme.txt file.

This program attempts to convert PIMS acceleration data (PAD) files into Audio
Interchange File Format (AIFF) files, and it can plot the demeaned acceleration
data too.

Given zero input arguments, this program shows this help text and quits.

Given multiple input filename arguments, this program attempts to read each as a
PAD file named <filename> and convert its contents to an AIFF file with suffix
"s.aiff"; where s designates sum(x+y+z) axis data.

You can change the default behavior with input argument options for mode, axis,
rate, taper.

When plot mode is invoked, this program produces a plot of the demeaned
acceleration data for the axis selected, e.g. <filenamex.png> would be the plot
output filename for input PAD file <filename> when the X-axis is selected.
    
EXAMPLES:

# to run demo
python ugaudio.py -m demo

# to convert a PAD file to AIFF using default parameters (replace filename)
python ugaudio.py filename

# to convert a PAD file to AIFF & plot demeaned accel PNG (replace filename)
python ugaudio.py -m plot filename

# to convert PAD files to AIFFs using rate of 22050 sa/sec & produce PNGs for accel plots
python ugaudio.py -r 22050 -m plot filename1 filename2

INPUT ARGUMENTS LISTED BELOW (see "usage" syntax above):
"""

import sys
import argparse

# Help parser get a non-negative value; otherwise, exception.
def check_nonnegative(value):
    """Help parser get a non-negative value; otherwise, exception."""
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is an invalid non-negative int value" % value)
    return ivalue

# A class to override argparse error message.
class MyParser(argparse.ArgumentParser):
    """A class to override argparse error message."""
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(1)

# Print arguments (nicely?).
def show_args(mode, axis, rate, taper, files):
    """Print arguments (nicely?)."""
    if not mode == 'demo':
        print "mode = %s," % mode,
        if rate:
            print "sample rate = {} sa/sec,".format(rate),
        else:
            print "sample rate = native,",
        print "axis = %s," % axis,
        print "taper = %sms," % str(taper),
        print "file argument count = %d" % len(files)
        if len(files) == 0:
            print "It looks like you neglected to include file(s) as command line arguments."
            print "No PAD-like filename argument(s), so nothing to do.  Try no arguments for help."
            print "Bye for now."
            sys.exit(3)
    else:
        print "mode = %s" % mode
    
    print '~' * 80

# Parse input arguments.
def parse_args():
    """Parse input arguments."""
    parser = MyParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-m', default="aiff", choices=['aiff', 'plot', 'demo'], help="mode choices")
    parser.add_argument('-a', default="s", choices=['x', 'y', 'z', 's', '4'], help="axis choices; default is s (for sum), use 4 for ALL")
    parser.add_argument('-r', default=0, type=check_nonnegative, help="integer R > 0 for sample rate to override native; default is R=0 for native rate")
    parser.add_argument('-t', default=0, type=check_nonnegative, help="integer T > 0 for milliseconds of taper; default is T=0 for no tapering")
    parser.add_argument('files', nargs='*', help="file(s) to process")
    args = parser.parse_args()
    
    # no input args, so just print help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(2)

    # return arguments: (m)ode, (a)xis, (r)ate, (t)aper, and files
    return args.m, args.a, args.r, args.t, args.files
