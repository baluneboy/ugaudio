#!/usr/bin/env python

import sys
import aifc
import struct
import numpy as np
from pims.utils.pimsdateutil import pad_fullfilestr_to_start_stop


def bin2asc_ted(filename, columns=4):
    """Ted Wright's original bin2asc routine convert file to ASCII."""    
    f = open(filename)
    d = f.read()
    f.close()
    sys.stdout = open(filename+'.ascii', 'w')
    for i in range(len(d)//4):
        v = struct.unpack('<f', d[i*4:i*4+4])  # force little Endian float
        print('%12.9e   ' % v, end=' ')
        if i % columns == columns-1:
            print()
    sys.stdout.close()


def pad_read(filename, columns=4, offset=0, count=-1, out_dtype=np.float32):
    """Return 2d numpy array of float32's read from filename input."""
    with open(filename, "rb") as f: 
        a = np.fromfile(f, offset=offset, count=count, dtype=np.float32)  # accel file: 32-bit float "singles"
    b = np.reshape(a, (-1, columns))
    if not b.dtype == out_dtype:
        b = b.astype(out_dtype)
    return b


def pad_readall(filename, columns=4, out_dtype=np.float32):
    """Return 2d numpy array of float32's read from filename input."""
    with open(filename, "rb") as f:
        a = np.fromfile(f, count=-1, dtype=np.float32)  # accel file: 32-bit float "singles"
    b = np.reshape(a, (-1, columns))
    if b.dtype == out_dtype:
        return b
    return b.astype(out_dtype)


def padread_vxyz(filename, columns=4, out_dtype=np.float32):
    """Return 2d numpy array of float32's read from filename input (demeaned, then 1st column replaced by vecmag)"""

    # load file
    a = pad_read(filename, columns=columns, out_dtype=out_dtype)

    # demean x, y and z columns
    a[:, 1:4] = a[:, 1:4] - a[:, 1:4].mean(axis=0)

    # compute vector magnitude
    v = np.array(np.sqrt(a[:, 1] ** 2 + a[:, 2] ** 2 + a[:, 3] ** 2))

    # overwrite times in 1st column with vecmag values
    a[:, 0] = v

    return a


def padread_hourpart(filename, fs, dh, columns=4, out_dtype=np.float32):
    """Return 2d numpy array of float32's read from filename input where dh_lower <= t < dh_upper."""

    # load file
    a = padread_vxyz(filename, columns=columns, out_dtype=out_dtype)

    # get start & stop time of file
    fstart, fstop = pad_fullfilestr_to_start_stop(filename)

    # find offset on lower end of file
    i1 = 0
    offset_lower = (dh - fstart).total_seconds()
    if offset_lower > 0:
        i1 = np.int(np.ceil(fs * offset_lower))

    dh_upper = dh + relativedelta(hours=1)

    # find offset on upper end of file
    i2 = a.shape[0]
    offset_upper = (fstop - dh_upper).total_seconds()
    if offset_upper > 0:
        i2 = np.int(np.ceil(fs * offset_upper))

    # print fstart, 'fstart'
    # print dh, 'dh'
    #
    # print offset_lower
    #
    # print fstop, 'fstop'
    # print dh_upper, 'dh_upper'
    #
    # print offset_upper
    # print i1, i2

    return a[i1:i2, :]


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
