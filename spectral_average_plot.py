#!/usr/bin/env python

import datetime
import glob
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import loadmat

from spectral_average_defaults import DEFAULT_OUTDIR, DEFAULT_NFFT, DEFAULT_PLOTRANGEPCT, LOCATIONS
from pims.utils.pimsdateutil import datetime_to_ymd_path


def plot_psd_xyz(pdf_file, psd_xyzv, deltaf, sensor, fs, fc, location, nfft, axs='xyzv', xlim=[0, 200], ylim=[1e-14, 1e-2]):
    """plot PSDs for x-, y- & z-axis overlay or 3-panel"""

    # create frequency vector based on deltaf
    N = psd_xyzv.shape[0]
    f = np.arange(0, N * deltaf, deltaf)

    # create figure and axes objects
    fig = plt.figure(figsize=(11, 8.5))
    ax = plt.subplot(111)

    axs = axs.lower()
    c = 0
    if 'x' in axs: linex, = ax.semilogy(f, psd_xyzv[:, 0], label='X-Axis', color='red'); c += 1
    if 'y' in axs: liney, = ax.semilogy(f, psd_xyzv[:, 1], label='Y-Axis', color='green'); c += 1
    if 'z' in axs: linez, = ax.semilogy(f, psd_xyzv[:, 2], label='Z-Axis', color='blue'); c += 1
    if 'v' in axs: linev, = ax.semilogy(f, psd_xyzv[:, 3], label='RSS(X,Y,Z)', color='black'); c += 1

    plt.ylim(ylim)
    plt.xlim(xlim)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [g**2/Hz]')
    plt.grid(True)

    plt.title(r'%s at %s (fs = %.1f sa/sec, $\Delta f$ = %.3f Hz)' % (sensor, location, fs, deltaf), fontsize=12)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=c, fancybox=True, shadow=True)

    an1 = ax.annotate('Nfft = %d' % nfft, xy=(0.94, 0.98), xycoords="axes fraction",
                      va="center", ha="center",
                      bbox=dict(boxstyle="round", fc="w"))

    plt.savefig(pdf_file)


def spec_avg_date_range_plot(sensor, location, day_start, day_stop, nfft, fs, fc,
                             out_dir=DEFAULT_OUTDIR,
                             axs='xyz',
                             xlim=[0, 200],
                             ylim=[1e-14, 1e-2]):
    dr = pd.date_range(day_start, day_stop, freq='1D')
    fs_str = str(fs).replace('.', 'p')
    mat_files = []
    for d in dr:
        yr, mo, da = d.year, d.month, d.day
        ym_path = os.path.dirname(datetime_to_ymd_path(d, base_dir=out_dir))
        # e.g. 2020-04-14_121f08_500p0_32768_psdsum.mat
        psdsum_bname = '%4d-%02d-%02d_%s_%s_%d_psdsum.mat' % (yr, mo, da, sensor, fs_str, nfft)
        mat_file = os.path.join(ym_path, psdsum_bname)
        if os.path.isfile(mat_file):
            mat_files.append(mat_file)

    pdf_bname = '%4d-%02d-%02d_%4d-%02d-%02d_%s_%s_%d_psdavg.pdf' % (day_start.year, day_start.month, day_start.day,
                                                                     day_stop.year, day_stop.month, day_stop.day,
                                                                     sensor, fs_str, nfft)
    ym_path = os.path.dirname(datetime_to_ymd_path(day_start, base_dir=out_dir))
    pdf_file = os.path.join(ym_path, pdf_bname)

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
    deltaf = mat_dict['deltaf'][0][0]

    plot_psd_xyz(mat_files[0].replace('psdsum.mat', 'psdavg.pdf'), psd_sum / psd_count, deltaf, sensor, fs, fc,
                 location, nfft, axs='xyz',
                 xlim=xlim, ylim=ylim)

    # print psd_count,
    # print psd_sum[3][1],
    for f in mat_files[1:]:
        m = loadmat(f)
        this_psd, this_count = m['psd'], m['count'][0][0]
        psd_sum += this_psd
        psd_count += this_count
        plot_psd_xyz(f.replace('psdsum.mat', 'psdavg.pdf'), this_psd / this_count, deltaf, sensor, fs, fc, location,
                     nfft, axs='xyz',
                     xlim=xlim, ylim=ylim)
        # print psd_count,
        # print psd_sum[3][1],

    # print psd_sum[3][1] / psd_count

    psd_xyzv = psd_sum / psd_count
    plot_psd_xyz(pdf_file, psd_xyzv, deltaf, sensor, fs, fc, location, nfft, axs=axs, xlim=xlim, ylim=ylim)


if __name__ == "__main__":

    # start/stop date
    day_start = datetime.date(2020, 4, 10)
    day_stop = datetime.date(2020, 4, 13)

    # parameters that need defining
    fs, fc = 500.0, 200.0
    nfft = DEFAULT_NFFT

    # iterate over sensors to produce daily and ensemble plots
    for sensor, location in LOCATIONS.iteritems():
        print sensor, location
        spec_avg_date_range_plot(sensor, location, day_start, day_stop, nfft, fs, fc,
                                 out_dir=DEFAULT_OUTDIR,
                                 axs='xyz',
                                 xlim=[0.0, 3.0],
                                 ylim=[1e-14, 1e-2],
                                 )
