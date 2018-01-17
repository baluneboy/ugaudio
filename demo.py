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

    print '\ndemo with actual acceleration data from %s (if file exists)' % data_file
    
    # get PadFile and attempt conversion
    pad_file = PadFile(data_file)
    
    if not pad_file.exists:
       raise Exception('data file "%s" does not exist', data_file)
       
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

def demo_build_numpy_array(sensor, y, m, d):
    import glob
    import datetime
    import numpy as np
    from ugaudio.load import padread
    from pims.utils.pimsdateutil import datetime_to_ymd_path
    ymd_dir = datetime_to_ymd_path(datetime.date(y, m, d))
    glob_pat = '%s/*_accel_%s/*%s' % (ymd_dir, sensor, sensor)
    fnames = glob.glob(glob_pat)
    fnames = ['/tmp/rogue_pad_file.sensor']
    arr = np.empty((0, 5), dtype=np.float32)    # float32 matches what we read from PAD file
    for fname in fnames:
        # read data from file (not using double type here like MATLAB would, so we get courser demeaning)
        a = padread(fname)
        a[:,1:4] = a[:,1:4] - a[:,1:4].mean(axis=0)  # demean x, y and z columns
        v = np.array( np.sqrt(a[:,1]**2 + a[:,2]**2 + a[:,3]**2) )  # compute vector magnitude
        print v
        #new_col = np.reshape(v, (-1, 1))
        ncols = 1
        v.shape = (v.size//ncols, ncols)
        #print v.shape, a.shape
        a = np.append(a, v, axis=1) # append to get 5th column for vecmag
        #print v.shape, a.shape
        arr = np.append(arr, a, axis=0)
        #print arr.shape        
    return arr    
    
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
    
    ## build numpy array (appending rows for each PAD file and appending vecmag column along the way)
    #arr = demo_build_numpy_array('121f03006', 2017, 11, 1)
    #print arr
