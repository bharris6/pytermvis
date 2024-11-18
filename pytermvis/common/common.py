import math

import numpy as np


def normalize(lower, upper, vals):
    """
    Normalize all values so that they're between the lower and the
    upper bounds that were passed in.

    :param lower: The lower bound
    :type lower: float

    :param upper: The upper bound
    :type upper: float

    :param vals: A list of numbers
    :type vals: list[float]

    :returns: The list of numbers redistributed across the new bounds
    :rtype: list[float]
    """
    return [(lower + (upper - lower)*v) for v in vals]


def remap(x, x1, x2, y1, y2):
    """
    Remaps value x to a new range.

    :param x: Value to act on

    :param x1: Old Minimum
    :param x2: Old Maximum

    :param y1: New Minimum
    :param y2: New Maximum

    :returns: The original value mapped to the new range.
    """
    if (x2 == x1 and x2 == 0) or (y2 == y1 and y2 == 0):
        return 0
    return (((x - x1) * (y2 - y1)) / (x2 - x1)) + y1


def power_scale(amps):
    """
    Calculate the logarithm of the max power in each range, instead of
    the average.

    :param amps: array of amplitudes

    :returns: The base-10 logarithm of the maximum of the squares of `amps`
    """
    mx = np.max(np.array(amps)**2)
    if mx != 0:
        return math.log10(mx)
    else:
        return 0


def get_fft(sample, rate):
    """
    Apply a Hamming window to the given signal sample and then generate an
    FFT of the signal sample.

    :param data: The signal sample
    :param rate: The sample rate for the signal

    :returns: The list of frequencies in the sample and the FFT of the sample
    """
    sample = sample * np.hamming(len(sample))
    fft = np.fft.fft(sample)
    freqs = np.fft.fftfreq(
        len(fft),
        1.0 / rate,
    )
    return freqs, fft


def bin_signal(signal, num_bins):
    bin_width = len(signal) // num_bins
    sig_binned = []
    for i in range(0, len(signal), bin_width):
        sig_binned.append(
            np.mean(np.abs(signal[i:i+bin_width]))
        )
    return sig_binned


def bin_fft(fftfreqs, fft, num_bins):
    """
    Make use of numpy to divide the FFT's frequencies into a fixed number of
    frequency bins.

    :param fftfreqs: The frequencies correlating to the values in the FFT
    :param fft: The value of the FFT for each frequency.

    :param num_bins: How many bins to split the FFT into.

    :returns: The "binned" FFT as an array of length `num_bins`
    """
    bin_width = len(fftfreqs) // num_bins
    fft_binned = []
    for i in range(0, len(fft), bin_width):
        fft_binned.append(np.mean(np.abs(fft[i:i+bin_width])))
    return fft_binned


def gamma_bin_fft(fftfreqs, fft, rate=44100, numbins=None, gamma=2.0):
    """
    map frequencies to bin indexes using the same function used to correct
    for perceived brightness on CRT monitors
    https://dlbeer.co.nz/articles/fftvis.html

    :param fftfreqs: The frequencies correlating to the values in the FFT
    :param fft: The value of the FFT for each frequency.

    :param num_bins: How many bins to split the FFT into.

    :param gamma: How heavy of an effect the correction should have.

    :returns: The "gamma-corrected-binned" FFT as an array of length `num_bins`
    """
    if numbins is not None:

        nfreqs = len(fftfreqs) // 2
        f_start = 0

        smoothing = (0.00007)**(len(fftfreqs) / rate)
        powers = [0]*numbins

        for i in range(numbins):
            bin_power = 0
            f_end = math.floor((((i+1) / numbins)**gamma)*nfreqs)
            if f_end > nfreqs:
                f_end = nfreqs

            f_width = f_end - f_start
            if f_width <= 0:
                f_width = 1

            for j in range(f_width):
                s = fft[f_start + j]
                p = abs(s)**2
                bin_power = max(p, bin_power)

            bin_power = max(bin_power, 1.0)
            bin_power = max(math.log(bin_power), 0.0)

            powers[i] = (
                (powers[i]*smoothing) + (bin_power * 0.05 * (1.0-smoothing))
            )
            f_start = f_end

        return fftfreqs, np.array(powers)

    else:
        return fftfreqs, fft
