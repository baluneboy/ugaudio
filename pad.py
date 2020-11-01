#!/usr/bin/env python

"""A loose interpretation of PAD (if you know what that means) for binary file
handling and audio conversion."""

import os
import re
import aifc
import struct
import numpy as np
import matplotlib.pyplot as plt
from ugaudio.load import pad_read
from ugaudio.signal import normalize, my_taper

class PadFile(object):
    """A class to implement a loose interpretation for binary file conversion to audio.

    This class will produce an object that can be used for converting the binary
    input file to Audio Interchange File Format (AIFF). The conversion will only
    succeed if the underlying input file's data are formatted as float32 binary
    values with txyz frames: t1, x1, y1, z1, t2, x2, y2, z2, ...

    For a given input data file (e.g. "/some/path/to/my_pad_file"), if there
    also exists a header file (e.g. "/some/path/to/my_pad_file.header"), then we
    attempt to parse the sample rate from the header file using a regular
    expression so that a line like this "<SampleRate>1234.5</SampleRate>" yields
    a sample rate of 1234.5 samples per second. In the absence of a readily
    identifiable (accompanying) header file, calculate the sample rate assuming
    that the time values in the data file are relative, in seconds, and start
    with zero as the first time value.

    """
    
    def __init__(self, filename):
        """Constructs a PadFile."""
        self.filename = filename
        self.headerfile = None
        self.samplerate = None
        self.ispad = False
        self.exists = False
        if self.is_pad():
            self.ispad = True
            self.headerfile = self.get_headerfile()
            self.samplerate = self.get_samplerate()

    def __str__(self):
        """str(self)"""
        bname = os.path.basename(self.filename)
        if self.ispad:
            return '%s, native rate = %.2f sa/sec' % (bname, self.samplerate)
        elif self.exists:
            return '%s (non-%s)' % (bname, self.__class__.__name__)
        else:
            return '%s (non-file)' % bname
    
    def is_pad(self):
        """Return True if file exists, has non-zero length, and float32 txyz frames."""
        if not os.path.exists(self.filename):
            return False
        self.exists = True
        fsize = os.path.getsize(self.filename)
        if fsize == 0:
            return False
        # FIXME hard-coded 4 as "column" size (MAMS will not work)
        if fsize % 4 != 0:
            return False
        return True
    
    def get_headerfile(self):
        """Return header filename if it exists; otherwise, None."""
        hdrfile = self.filename + '.header'
        if os.path.exists(hdrfile):
            return hdrfile
        else:
            return None
    
    def _calculate_sample_rate(self):
        """Calculate sample rate from time step in data file."""
        with open(self.filename, 'rb') as f:
            # FIXME THIS IS ONLY VALID WITH 4-COLUMN PAD FILES.
            # Note that *most* PAD files use relative time in seconds with t1 =
            # 0 and next time starting at byte 16, so seek to that position
            f.seek(4*4)
        
            # Now we want just one of these 4-byte floats (float32)
            b = f.read(4)
        
        # Decode time step (delta t) as little-endian float32.
        delta_t = struct.unpack('<f', b)[0]
        
        # Return calculated sample rate.
        return round(1.0 / delta_t, 3)
    
    def get_samplerate(self):
        """Attempt to parse sample rate from header file; otherwise calculate it."""
        if self.headerfile:
            with open(self.headerfile, 'r') as f:
                contents = f.read().replace('\n', '')
                m = re.match('.*\<SampleRate\>(.*)\</SampleRate\>.*', contents)
                if m:
                    return float( m.group(1) )
                else:
                    return None
        else:
            return self._calculate_sample_rate()
    
    def convert(self, rate=None, axis='s', plot=False, taper=0):
        """Convert designated axis to AIFF, and maybe plot it too."""
        # If not properly formatted, then return without doing anything.
        if not self.ispad:
            return
    
        # Get sample rate.
        if not rate:
            samplerate = self.samplerate
        else:
            samplerate = rate
                
        # Read data from file.
        B = pad_read(self.filename)
    
        # Demean each column.
        M = B.mean(axis=0)
        C = B - M[np.newaxis, :]
       
        # Determine desired axis or axes.
        if axis == '4': axis = 'xyzs'
        for ax in axis.lower():
            if ax == 'x': data = C[:, -3] # x-axis is 3rd last column
            elif ax == 'y': data = C[:, -2] # y-axis is 2nd last column
            elif ax == 'z': data = C[:, -1] # z-axis is the last column
            elif ax == 's': data = C[:, 1::].sum(axis=1) # sum(x+y+z)
            else:
                raise Exception( 'unhandled axis "%s"' % ax )
            stub = self.filename + ax
            
            # Plot demeaned accel data (maybe).
            if plot:
                png_file = stub + '.png'
                plt.plot(data)
                plt.savefig(png_file)
            
            # Normalize to range -32768:32767 (actually, use -32000:32000).
            data = normalize(data) * 32000.0
            
            # Taper signal, if requested.
            if taper > 0:
                data = my_taper(data, samplerate, taper/1000.0)
        
            # Data conditioning.
            data = np.rint(data) # round to nearest integer
            data = data.astype(np.int16) # not sure why we need this...maybe aifc assumptions
            data = data.byteswap().newbyteorder() # need this on mac osx and linux (windows?)
        
            # Convert data to string for aifc write to work right.
            strdata = data.tostring()
            aiff_file = stub + '.aiff'
            g = aifc.open(aiff_file, 'w')
            sampwidth = 2 # this value based on data type (2 bytes in np.int16)
            #         nchans, sampwidth, framerate, nframes, comptype, compname
            g.setparams((1, sampwidth, samplerate, len(data), 'NONE', 'not compressed'))
            g.writeframes(strdata)
            g.close()
