#!/usr/bin/env python

import aifc
import os.path
import numpy as np
import matplotlib.pyplot as plt
from ugaudio.load import padread
from ugaudio.create import get_chirp
from ugaudio.signal import normalize
from ugaudio.pad import PadFile

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

def demo_accel_file(data_file, axis='x'):
    """demo arbitrary file with microgravity accel data from ISS"""

    print '\ndemo with actual acceleration data from %s' % data_file
    
    # get PadFile and attempt conversion
    pad_file = PadFile(data_file)
    
    try:
        pad_file.convert(plot=True, axis=axis)
        msg = 'wrote PNG & AIFF files for %s-axis of %s' % (axis, pad_file)
    
    except:
        msg = 'could not convert to audio (or plot) %s' % pad_file
    
    print msg + '\n'

def show_samplerate(header_file):
    """return sample rate (samples/sec) for input header file"""
    pad_file = PadFile(header_file)
    print pad_file
    
if __name__ == "__main__":
    
    ## get sample rate from header file
    #header_file = '/misc/yoda/pub/pad/year2017/month04/day01/sams2_accel_121f04/2017_04_01_20_55_05.415+2017_04_01_21_05_05.426.121f04.header'
    #data_file = header_file.replace('.header', '')
    #show_samplerate(data_file)
    
    ## generate artficial chirp, then create sound file (AIFF format) and plot it (PNG format)
    #demo_chirp()
    
    # plot SAMS TSH (es06) data file (just one axis)
    data_file = '/tmp/2017_05_22_23_39_02.803+2017_05_22_23_49_02.861.es06'
    #show_samplerate(data_file)
    demo_accel_file(data_file, axis='x') # just x-axis here