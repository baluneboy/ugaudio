import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def demo_plot_psd_xyz(pdf_file, psd_xyz, deltaf, sensor, fs, fc, location, nfft):
    """plot PSDs for x-, y- & z-axis overlay or 3-panel"""

    # create frequency vector based on deltaf
    N = psd_xyz.shape[0]
    f = np.arange(0, N * deltaf, deltaf)

    # create figure and axes objects
    fig = plt.figure(figsize=(11, 8.5))
    ax = plt.subplot(111)

    linex, = ax.semilogy(f, psd_xyz[:, 0], label='X-Axis', color='red')
    liney, = ax.semilogy(f, psd_xyz[:, 1], label='Y-Axis', color='green')
    linez, = ax.semilogy(f, psd_xyz[:, 2], label='Z-Axis', color='blue')

    plt.ylim([1e-7, 100])
    plt.xlim([0, fc])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [g**2/Hz]')
    plt.grid(True)

    plt.title(r'%s at %s (fs = %.1f sa/sec, $\Delta f$ = %.3f Hz)' % (sensor, location, fs, deltaf), fontsize=12)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=3, fancybox=True, shadow=True)

    an1 = ax.annotate('Nfft = %d' % nfft, xy=(0.95, 0.98), xycoords="axes fraction",
                      va="center", ha="center",
                      bbox=dict(boxstyle="round", fc="w"))

    plt.savefig(pdf_file)


# Generate a test signal, a 2 Vrms sine wave at 1234 Hz, corrupted by 0.001 V**2/Hz of white noise sampled at 10 kHz.
fs = 500
N = 1e3
nfft = 512
amp = 2*np.sqrt(2)
freq = 123.4
noise_power = 0.001 * fs / 2
time = np.arange(N) / fs
x = amp*np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

# Compute and plot the power spectral density.
f, Pxx_den = signal.welch(x, fs, nperseg=nfft)

deltaf = f[1]
psd_xyz = np.c_[Pxx_den, Pxx_den / 4, Pxx_den * 5]
# print psd_xyz.shape

sensor = '121f08006'
fc = 200
location = 'JPM1F1, ER5, Inside RTS/D2'

demo_plot_psd_xyz('c:/temp/trash.pdf', psd_xyz, deltaf, sensor, fs, fc, location, nfft)
