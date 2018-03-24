#!/usr/bin/env python

import glob
import os.path
import numpy as np
import matplotlib.pyplot as plt


def get_accel_dir(day, unit, head, usmp4_dir='/home/ken/data/usmp4'):
    """return accel subdirectory string given integer day and strings for unit, head and usmp4 dir"""
    # like /home/ken/data/usmp4/usmp_4F_1/HEADB/DAY000/ACCEL
    u = 'usmp_4%s_1' % unit
    h = 'HEAD%s' % head
    d = 'DAY%03d' % day
    return os.path.join(usmp4_dir, u, h, d, 'ACCEL')


def get_hour_files(axis, day, hour, unit, head, usmp4_dir='/home/ken/data/usmp4'):
    """return list of accel data files for given axis, day, hour, etc."""
    acc_dir = get_accel_dir(day, unit=unit, head=head, usmp4_dir=usmp4_dir)
    glob_pat = os.path.join(acc_dir, '%s%sM%03d%02d.*' % (head, axis, day, hour))  # full filename to like BXM00018.55R
    files = sorted(glob.glob(glob_pat))
    return files


def build_numpy_array(fnames):
    """build numpy array from data read from list of filenames"""
    from ugaudio.load import padread
    arr = np.empty((0, 1), dtype=np.float32)
    print 'building array...'
    for fname in fnames:
        # read data from file
        a = padread(fname, columns=1)
        a[:, 0] = a[:, 0] - a[:, 0].mean(axis=0)  # demean column(s)
        print '+ %d data pts from %s' % (a.shape[0], fname)
        arr = np.append(arr, a, axis=0)
    return arr[:, 0]


def get_sleep_to_wake_files(usmp4_dir):
    """get list of accel data files that show sleep to wake transition"""
    axis, day, unit, head = 'X', 0, 'F', 'B'
    some_files = []
    for hr in [18, 19]:
        some_files += get_hour_files(axis, day, hr, unit, head, usmp4_dir=usmp4_dir)
    return some_files


def plot_sleep_to_wake_data():

    # example to load sleep-to-wake transition data
    usmp4_dir = '/home/ken/data/usmp4'
    xfiles = get_sleep_to_wake_files(usmp4_dir)
    x = build_numpy_array(xfiles)
    print '%d total data pts in array' % x.shape[0]

    # plot color spectrogram to see crew wake
    NFFT = 4096  # the length of the windowing segments (finer freq. resolution comes from larger NFFT)
    Fs = 125.0  # samples per second

    # build time array (seconds relative to first file start)
    dt = 1.0 / Fs
    t = np.arange(0.0, x.shape[0] / Fs, dt)

    # figure for plots
    fig = plt.figure(num=None, figsize=(8, 6), dpi=120, facecolor='w', edgecolor='k')

    # plot x-axis accel. time domain data
    ax1 = plt.subplot(211)
    plt.plot(t, x)
    plt.ylabel('X-Axis Accel. [g]')

    # plot x-axis spectrogram frequency domain data (to better see crew wake transition)
    # Pxx is the segments x freqs array of instantaneous power, freqs is
    # the frequency vector, bins are the centers of the time bins in which
    # the power is computed, and im is the matplotlib.image.AxesImage
    # instance
    ax2 = plt.subplot(212, sharex=ax1)
    Pxx, freqs, bins, im = plt.specgram(x[:], NFFT=NFFT, Fs=Fs, noverlap=NFFT/2, cmap='jet', vmin=-140, vmax=-70)

    # set y-limits for cut-off frequency of this sensor head (25 Hz)
    plt.ylim((0, 25))

    # add labeling
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Relative Time [sec]')

    # add colorbar
    fig.colorbar(im)

    # fix ax position
    pos1, pos2 = ax1.get_position(), ax2.get_position()  # get the original positions
    pos1 = [pos1.x0, pos1.y0, pos2.width, pos1.height]
    ax1.set_position(pos1)  # set a new position

    plt.show()


if __name__ == "__main__":
    # Compare plot to Appendix page B-7 of Summary Report of Mission Acceleration Measurements for STS-87
    plot_sleep_to_wake_data()

