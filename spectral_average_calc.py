#!/usr/bin/env python

import datetime
import glob
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.io import savemat
from ugaudio.load import pad_read
from pims.utils.pimsdateutil import datetime_to_ymd_path
from pims.files.filter_pipeline import FileFilterPipeline, MinDurMinutesPad, HeaderMatchesRateCutoffLocSsaPad
from pims.files.utils import mkdir_p


class PsdAccumulator(object):
    """A class to accumulate PSDs for spectral averaging.

    This class will calculate a running sum of PSDs and keep
    count of how many to average when done accumulating.

    """

    def __init__(self, fs, nperseg=32768):
        self.fs = fs
        self.nperseg = nperseg
        self.f, self.psd = None, None
        self.count = 0

    def append(self, txyz, verbose=False):
        """compute array of PSDs from acceleration vs. time value input array, append & increment"""

        # delete first (time) column
        xyz = np.delete(txyz, 0, axis=1)

        # calculate how many segments we can fit into data length
        N = xyz.shape[0]
        numsegs = N // self.nperseg
        numpts = self.nperseg * numsegs

        # complain about not enough data for at least one segment and early return
        if verbose:
            if numsegs < 1:
                print '%d pts is not enough even one segment of length %d' % (N, self.nperseg)
                return
            else:
                print 'numsegs = %d, nperseg = %d, numpts = %d' % (numsegs, self.nperseg, numpts)

        # increment counter
        self.count += 1

        # now do actual trim (resize) here
        xyz = np.resize(xyz, (numpts, 3))

        # compute PSD for each column (each axis)
        f, Pxx = welch(xyz, self.fs, nperseg=self.nperseg, axis=0)

        # calculate overall PSD
        v = np.array(np.sqrt(Pxx[:, 0] ** 2 + Pxx[:, 1] ** 2 + Pxx[:, 2] ** 2))  # RSS(Pxx,Pyy,Pzz)

        # append RSS as 4th column
        Pxx = np.append(Pxx, np.reshape(v, (Pxx.shape[0], -1)), axis=1)

        if self.psd is None:
            self.psd = Pxx
        else:
            self.psd += Pxx

        if self.count == 1:
            self.f = f

    def spectral_avg(self):
        return self.psd / self.count

    def save_psdsum_matfile(self, file_name):
        mdict = {'deltaf': self.f[1],
              'psd': self.psd,
              'count': self.count
              }
        savemat(file_name, mdict)

    def pdf_plot(self):
        spec_avg = self.spectral_avg()
        plt.semilogy(self.f, spec_avg)
        plt.xlabel('frequency [Hz]')
        plt.ylabel('PSD [g**2/Hz]')
        plt.show()


class PsdRunningTally(object):
    """A class to manage running tally of PSDs for spectral averaging.

    This class will orchestrate a running tally of PSDs given information on PAD files to be considered.

    """

    def __init__(self, pad_files, pa):
        self.pad_files = pad_files
        self.pa = pa

    def run(self):
        file_count = 0
        print '\nBEGIN'
        for fname in self.pad_files:
            file_count += 1
            a = pad_read(fname)
            a[:, 1:4] = a[:, 1:4] - a[:, 1:4].mean(axis=0)  # demean x, y and z columns
            self.pa.append(a)
            print file_count, os.path.basename(fname)
        print 'END'


def spec_avg_one_day(sensor, y, m, d, nfft, fs, fc, location, minMinutes=5.5, num_files=None, pad_dir='D:/pad',
                     out_dir='C:/temp/psdsum'):

    # create PSD accumulator object
    pa = PsdAccumulator(fs, nperseg=nfft)

    # get a list of qualifying PAD files to consider
    ffp = FileFilterPipeline(MinDurMinutesPad(minMinutes), HeaderMatchesRateCutoffLocSsaPad(fs, fc, location))
    print ffp

    ymd_dir = datetime_to_ymd_path(datetime.date(y, m, d), base_dir=pad_dir)
    glob_pat = '%s/*_accel_%s/*%s' % (ymd_dir, sensor, sensor)
    fnames = glob.glob(glob_pat)

    print glob_pat
    print 'we have %d files before filtering' % len(fnames),
    filt_fnames = list(ffp(fnames))
    print 'and %d files after filtering' % len(filt_fnames)

    if num_files is None:
        num_files = len(filt_fnames)
    print 'NOTE: We are SKIPPING some for testing, so we only have %d files now\n' % num_files
    fnames = filt_fnames[0:num_files]

    # create object for PSD running tally
    prt = PsdRunningTally(fnames, pa)

    # do running tally
    prt.run()

    # save pdf plot (e.g. "C:\temp\psdsum\year2020\month04\2020-04-07_121f03_500p0_32768_psdsum.mat")
    fs_str = str(fs).replace('.', 'p')
    psdsum_bname = '%4d-%02d-%02d_%s_%s_%d_psdsum.mat' % (y, m, d, sensor, fs_str, pa.nperseg)
    psdsum_dname = os.path.join(out_dir, 'year%d' % y, 'month%02d' % m)
    if not os.path.exists(psdsum_dname):
        mkdir_p(psdsum_dname)
    psdsum_file = os.path.join(psdsum_dname, psdsum_bname)
    prt.pa.save_psdsum_matfile(psdsum_file)

    # # create pdf plot
    # prt.pa.pdf_plot()

    return prt


def spec_avg_date_range(sensor, location, day_start, day_stop, nfft, fs, fc, num_files=None, pad_dir='d:/pad',
                        out_dir='c:/temp/psdsum', do_plot=True):
    dr = pd.date_range(day_start, day_stop, freq='1D')
    daily_running_tallies = []
    for d in dr:
        yr, mo, da = d.year, d.month, d.day
        prt = spec_avg_one_day(sensor, yr, mo, da, nfft, fs, fc, location, num_files=num_files, pad_dir=pad_dir,
                               out_dir=out_dir)
        if do_plot:
            prt.pa.pdf_plot()
        daily_running_tallies.append(prt)
    return daily_running_tallies


if __name__ == "__main__":

    pad_dir = 'D:/pad'

    # sensor, location = '121f03', 'LAB1O1, ER2, Lower Z Panel'
    # sensor, location = '121f05', 'JPM1F1, ER5, Inside RTS/D2'
    sensor, location = '121f08', 'COL1A3, EPM, near PK-4'
    fs, fc = 500.0, 200.0

    day_start = datetime.date(2020, 4, 5)
    day_stop = datetime.date(2020, 4, 9)

    nfft = 32768

    spec_avg_date_range(sensor, location, day_start, day_stop, nfft, fs, fc, num_files=None, pad_dir=pad_dir,
                        out_dir='c:/temp/psdsum', do_plot=False)

    print 'done'
