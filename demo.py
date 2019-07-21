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


def demo_build_numpy_array(sensor, y, m, d, minMinutes=2.0, num_files=None):
    import glob
    import datetime
    import numpy as np
    from ugaudio.load import padread
    from pims.utils.pimsdateutil import datetime_to_ymd_path
    from pims.files.filter_pipeline import FileFilterPipeline, MinDurMinutesPad, HeaderMatchesRateCutoffLocSsaPad
    
    location = 'LAB1P2, ER7, Cold Atom Lab Front Panel'
    fs, fc = 500, 200
    
    ffp = FileFilterPipeline(MinDurMinutesPad(minMinutes), HeaderMatchesRateCutoffLocSsaPad(fs, fc, location))
    print ffp
    
    ymd_dir = datetime_to_ymd_path(datetime.date(y, m, d))
    glob_pat = '%s/*_accel_%s/*%s' % (ymd_dir, sensor, sensor)
    fnames = glob.glob(glob_pat)
    
    print 'we have %d files before filtering' % len(fnames),
    filt_fnames = list( ffp(fnames) )
    print 'and %d files after filtering' % len(filt_fnames)    
    
    if num_files is None:
        num_files = len(filt_fnames)
    
    file_count = 0
    arr = np.empty((0, 5), dtype=np.float32)  # float32 matches what we read from PAD file
    print '\nBEGIN'
    for fname in filt_fnames[0:num_files]:
        # read data from file (not using double type here like MATLAB would, so we get courser demeaning)
        file_count += 1
        a = padread(fname)
        a[:,1:4] = a[:,1:4] - a[:,1:4].mean(axis=0)  # demean x, y and z columns
        v = np.array( np.sqrt(a[:,1]**2 + a[:,2]**2 + a[:,3]**2) )  # compute vector magnitude
        #print v
        #new_col = np.reshape(v, (-1, 1))
        ncols = 1
        v.shape = (v.size//ncols, ncols)
        #print v.shape, a.shape
        a = np.append(a, v, axis=1) # append to get 5th column for vecmag
        #print v.shape, a.shape
        arr = np.append(arr, a, axis=0)
        #print arr.shape
        print file_count, arr.shape, fname
    print 'END'
    return arr    


def demo_batch2(sensor, y, m, d, num_files=None):
    arr = demo_build_numpy_array(sensor, y, m, d, num_files=num_files)
    
    fig = plt.figure(figsize=(7.5, 10.0))

    axes1 = fig.add_subplot(3, 1, 1)
    axes2 = fig.add_subplot(3, 1, 2)
    axes3 = fig.add_subplot(3, 1, 3)

    axes1.set_ylabel('x-axis')
    # axes1.plot(np.mean(arr, axis=0))
    axes1.plot(arr[:, 1])

    axes2.set_ylabel('y-axis')
    # axes2.plot(np.max(arr, axis=0))
    axes2.plot(arr[:, 2])

    axes3.set_ylabel('z-axis')
    # axes3.plot(np.min(arr, axis=0))
    axes3.plot(arr[:, 3])

    fig.tight_layout()
    plt.show()
    

def demo_batch_files():

    import glob
    from ugaudio.load import padread

    sensor = '121f04'
    pad_dir = '/Users/ken/Downloads/pad'
    glob_pat = '%s/*%s' % (pad_dir, sensor)
    filenames = glob.glob(glob_pat)

    arr = np.empty((0, 5), dtype=np.float32)    # float32 matches what we read from PAD file

    # FIXME how best to filter filenames at this point for like common header, min file dur, etc.

    # TODO in filenames iteration, we need to add to histogram buckets, update count, etc. for running hist

    for fname in filenames:
        # read data from file (not using double type here like MATLAB would, so we get courser demeaning)
        a = padread(fname)
        a[:, 1:4] = a[:, 1:4] - a[:, 1:4].mean(axis=0)  # demean x, y and z columns
        v = np.array(np.sqrt(a[:, 1]**2 + a[:, 2]**2 + a[:, 3]**2))  # compute vector magnitude
        #print v
        #new_col = np.reshape(v, (-1, 1))
        ncols = 1
        v.shape = (v.size//ncols, ncols)
        # print v.shape, a.shape
        a = np.append(a, v, axis=1)  # append to get 5th column for vecmag
        # print v.shape, a.shape
        arr = np.append(arr, a, axis=0)
        print arr.shape, fname

    fig = plt.figure(figsize=(7.5, 10.0))

    axes1 = fig.add_subplot(3, 1, 1)
    axes2 = fig.add_subplot(3, 1, 2)
    axes3 = fig.add_subplot(3, 1, 3)

    axes1.set_ylabel('x-axis')
    # axes1.plot(np.mean(arr, axis=0))
    axes1.plot(arr[:, 1])

    axes2.set_ylabel('y-axis')
    # axes2.plot(np.max(arr, axis=0))
    axes2.plot(arr[:, 2])

    axes3.set_ylabel('z-axis')
    # axes3.plot(np.min(arr, axis=0))
    axes3.plot(arr[:, 3])

    fig.tight_layout()
    plt.show()
 
    
if __name__ == "__main__":

    sensor = '121f04'
    y, m, d = 2018, 6, 13
    demo_batch2(sensor, y, m, d, num_files=3)
    raise SystemExit

    ## get sample rate from header file
    #header_file = '/misc/yoda/pub/pad/year2017/month04/day01/sams2_accel_121f04/2017_04_01_20_55_05.415+2017_04_01_21_05_05.426.121f04.header'
    #data_file = header_file.replace('.header', '')
    #show_samplerate(data_file)
    
    ## generate artficial chirp, then create sound file (AIFF format) and plot it (PNG format)
    #demo_chirp()
    
    # plot SAMS TSH (es06) data file (just one axis)
    data_file = '/Users/ken/Downloads/pad/2018_06_13_11_33_51.247+2018_06_13_11_43_51.250.121f04'
    data_file = '/Users/ken/Downloads/pad/2018_06_13_22_04_05.377+2018_06_13_22_14_05.381.121f04'
    #show_samplerate(data_file)
    demo_accel_file(data_file, axis='x') # just x-axis here
    
    ## build numpy array (appending rows for each PAD file and appending vecmag column along the way)
    #arr = demo_build_numpy_array('121f03006', 2017, 11, 1)
    #print arr
