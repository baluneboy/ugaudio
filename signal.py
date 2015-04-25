#!/usr/bin/env python

import copy
import warnings
import numpy as np
from scipy.signal import hann

# Return amplitude normalized version of input signal.
def normalize(a):
    """Return amplitude normalized version of input signal."""
    sf = max(abs(a))
    if sf == 0:
        return a
    return a / sf

# Return numpts (desired = fs * t); but no more than one-third signal duration.
def clip_at_third(sig, fs, t):
    """Return numpts (desired = fs * t); but no more than one-third signal duration."""
    # number of pts to taper (maybe)
    Ndesired = int(fs * t)
    
    # ensure that taper is, at most, a third of signal duration
    third = len(sig) // 3
    if Ndesired > third:
        Nactual = third
        warnings.warn( 'Desired taper %d pts > ~one-third (%d pts) of signal. Just tapering a third of signal duration.' % (Ndesired, Nactual), RuntimeWarning )
    else:
        Nactual = Ndesired
    #print Ndesired, Nactual, len(sig), third
    return Nactual

# Return tapered copy of input signal; taper first & last t seconds.
def my_taper(a, fs, t):
    """Return tapered copy of input signal; taper first & last t seconds."""
    # number of pts to taper (at most, one-third of signal)
    N = clip_at_third(a, fs, t)
    
    # use portion of hann (w) to do the tapering
    w = hann(2*N+1)
    
    # taper both ends of signal copy (leave input alone)
    b = a.copy()
    b[0:N] *= w[0:N]
    b[-N:] *= w[-N:]
    return b

# Return time array derived from sample rate and length of input signal.
def timearray(y, fs):
    """Return time array derived from sample rate and length of input signal."""
    T = len(y) / float(fs) # total time of the signal
    return np.linspace(0, T, len(y), endpoint=False)
