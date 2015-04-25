#!/usr/bin/env python

import aifc
import os.path
import numpy as np
import matplotlib.pyplot as plt
from ugaudio.load import padread
from ugaudio.create import get_chirp
from ugaudio.signal import normalize
from ugaudio.pad import PadFile

# simple demo of chirp signal (not representative of accel data)
def demo_chirp(fs=44100):
    """simple demo of chirp signal (not representative of ug accel data)"""

    print '\ndemo with artificial chirp signal (not representative of ug accel data)'

    # get signal of interest
    y = get_chirp()

    # demean signal
    data = y - y.mean(axis=0)

    # normalize to range -32768:32767 (actually, use -32000:32000)
    data = data * 32000.0
    
    # data conditioning
    data = data.astype(np.int16) # not sure why we need this...maybe aifc assumptions
    data = data.byteswap().newbyteorder() # need this on mac osx and linux (windows?)
    
    # convert data to string for aifc to work write
    strdata = data.tostring()
    aiff_file = 'demo_chirp.aiff'
    g = aifc.open(aiff_file, 'w')
    sampwidth = 2
    #nchannels, sampwidth, framerate, nframes, comptype, compname
    g.setparams((1, sampwidth, fs, len(data), 'NONE', 'not compressed'))
    g.writeframes(strdata)
    g.close()
    print 'wrote demo chirp sound file %s' % aiff_file
    
    # plot data
    png_file = 'demo_chirp.png'   
    plt.plot(data)
    plt.savefig(png_file)    
    print 'wrote demo accel plot file  %s' % png_file

# somewhat representative of microgravity accel data from ISS
def demo_accel():
    """somewhat representative of microgravity accel data from ISS"""

    print '\ndemo with actual acceleration data from GMT 17-Oct-2014'

    # get PAD file from example dir
    _DIR = os.path.dirname(__file__)
    filename = os.path.join(_DIR, 'examples/2014_10_17_06_31_15.515+2014_10_17_06_41_15.528.121f02')
    
    if not os.path.exists(filename):
        print 'BUT COULD NOT FIND\n%s\nso abort demo\n' % filename
        raise SystemExit
    
    # get PadFile and attempt conversion
    pad_file = PadFile(filename)
    
    try:
        pad_file.convert(plot=True)
        msg = 'wrote PNG & AIFF files for...\n%s\nsee your "examples" directory' % pad_file
    
    except:
        msg = 'could not convert...\n%s\nis everything okay with "examples" directory?' % pad_file
    
    print msg + '\n'
