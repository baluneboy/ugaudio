#!/usr/bin/env python

import datetime
import glob
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat

from spectral_average_defaults import DEFAULT_OUTDIR, DEFAULT_NFFT, DEFAULT_PLOTRANGEPCT
from pims.utils.pimsdateutil import datetime_to_ymd_path


def pdf_plot(self):
    spec_avg = self.spectral_avg()
    plt.semilogy(self.f, spec_avg)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [g**2/Hz]')
    plt.show()
    plt.savefig('c:/temp/trash.pdf')


def spec_avg_date_range_plot(sensor, location, day_start, day_stop, nfft, fs, fc, out_dir=DEFAULT_OUTDIR):
    dr = pd.date_range(day_start, day_stop, freq='1D')
    mat_files = []
    for d in dr:
        yr, mo, da = d.year, d.month, d.day
        ym_path = os.path.dirname(datetime_to_ymd_path(d, base_dir=out_dir))
        fs_str = str(fs).replace('.', 'p')
        # e.g. 2020-04-14_121f08_500p0_32768_psdsum.mat
        psdsum_bname = '%4d-%02d-%02d_%s_%s_%d_psdsum.mat' % (yr, mo, da, sensor, fs_str, nfft)
        mat_file = os.path.join(ym_path, psdsum_bname)
        if os.path.isfile(mat_file):
            mat_files.append(mat_file)

    # verify we have min pct of files to be worth plot effort
    pct_files = 100.0 * len(mat_files) / len(dr)
    if pct_files >= DEFAULT_PLOTRANGEPCT:
        print 'got %.1f%% of files (more than %.1f%% min), so proceed' % (pct_files, DEFAULT_PLOTRANGEPCT)
    else:
        print 'did NOT get %.1f%% of files expecting (only got %.1f%%), so abort' % (DEFAULT_PLOTRANGEPCT, pct_files)
        return

    # get average of daily psdsum files
    mat_dict = loadmat(mat_files[0])
    psd_sum = mat_dict['psd']
    psd_count = mat_dict['count'][0][0]
    # print psd_count,
    print psd_sum[3][1],
    for f in mat_files[1:]:
        m = loadmat(f)
        psd_sum += m['psd']
        psd_count += m['count'][0][0]
        # print psd_count,
        print psd_sum[3][1],

    print psd_sum[3][1] / psd_count
    print ' done'




if __name__ == "__main__":

    fs, fc = 500.0, 200.0
    nfft = DEFAULT_NFFT

    # sensor, location = '121f03', 'LAB1O1, ER2, Lower Z Panel'
    # sensor, location = '121f05', 'JPM1F1, ER5, Inside RTS/D2'
    sensor, location = '121f08', 'COL1A3, EPM, near PK-4'

    day_start = datetime.date(2020, 4, 5)
    day_stop = datetime.date(2020, 4, 8)

    spec_avg_date_range_plot(sensor, location, day_start, day_stop, nfft, fs, fc, out_dir=DEFAULT_OUTDIR)
