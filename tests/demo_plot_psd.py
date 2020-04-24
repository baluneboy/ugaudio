import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def plot_psd_xyz(psd_xyz, deltaf, sensor, fs, fc, location):
    """plot PSDs for x-, y- & z-axis overlay or 3 panel"""

    # create frequency vector based on deltaf
    N = psd_xyz.shape[0]
    f = np.arange(0, N * deltaf, deltaf)

    lines = plt.semilogy(f, psd_xyz)
    plt.ylim([1e-7, 100])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    lines[0].set_c('red')
    lines[1].set_c('green')
    lines[2].set_c('blue')
    plt.show()


# Generate a test signal, a 2 Vrms sine wave at 1234 Hz, corrupted by 0.001 V**2/Hz of white noise sampled at 10 kHz.
fs = 500
N = 1e3
amp = 2*np.sqrt(2)
freq = 123.4
noise_power = 0.001 * fs / 2
time = np.arange(N) / fs
x = amp*np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

# Compute and plot the power spectral density.
f, Pxx_den = signal.welch(x, fs, nperseg=512)

deltaf = f[1]
psd_xyz = np.c_[Pxx_den, Pxx_den / 4, Pxx_den * 5]
# print psd_xyz.shape

sensor = 'Sensor'
fc = 200
location = 'Location'

plot_psd_xyz(psd_xyz, deltaf, sensor, fs, fc, location)
