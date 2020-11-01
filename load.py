#!/usr/bin/env python

import sys
import aifc
import struct
import numpy as np


def bin2asc_ted(filename, columns=4):
    """Ted Wright's original bin2asc routine convert file to ASCII."""    
    f = open(filename)
    d = f.read()
    f.close()
    sys.stdout = open(filename+'.ascii', 'w')
    for i in range(len(d)//4):
        v = struct.unpack('<f', d[i*4:i*4+4])  # force little Endian float
        print('% 12.9e   ' % v, end=' ')
        if i % columns == columns-1:
            print()
    sys.stdout.close()


def pad_read(filename, columns=4, offset=0, count=-1, out_dtype=np.float32):
    """Return 2d numpy array of float32's read from filename input."""
    with open(filename, "rb") as f: 
        a = np.fromfile(f, offset=offset, count=count, dtype=np.float32)  # accel file: 32-bit float "singles"
    b = np.reshape(a, (-1, columns))
    if b.dtype == out_dtype:
        return b
    return b.astype(out_dtype)


def aiffread(aiff_file):
    """Return data loaded from aiff file.

    First output is audio data array, and ...
    
    Params tuple is (in this order)
    - num_chans   = number of audio channels; 1 is mono
    - samp_width  = number of bytes per audio sample (use 2)
    - sample_rate = sample rate in samples per second
    - num_frames  = number of audio frames (rows in np array)
    - comp_type   = compression type: 'NONE'
    - comp_name   = compression name: 'not compressed'    
    """
    data = ''
    f = aifc.open(aiff_file, 'r')
    params = f.getparams()
    while True:
        newdata = f.readframes(512)
        if not newdata:
            break
        data += newdata
    f.close()
    arr = np.fromstring(data, np.short).byteswap()
    return arr, params


def sams_pad_read(f, offset_rows, count_rows=-1):
    """read count_rows from file, f, starting at offset_rows (omit time column)"""
    offset = offset_rows * 16
    count = -1 if count_rows == -1 else count_rows * 4
    return pad_read(f, offset=offset, count=count)[:, -3:].copy()
