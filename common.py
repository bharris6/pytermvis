import numpy as np
from scipy.fft import fft

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

def get_spectrum(y, Fs):
    """
    Given a signal, y, compute its frequency domain using a Fast 
    Fourier Transform (FFT).  Return the one-sided representation.

    :param y: The signal (list of values)
    :type y: list[float]

    :param Fs: The sampling frequency used for the signal
    :type Fs: int

    :returns: A tuple of the frequency range and the absolute amplitude of
              each frequency.
    :rtype: tuple
    """
    signal_length = len(y)
    k = np.arange(signal_length)
    T = signal_length / Fs
    frq = k / T # two-sides frequency range
    frq = frq[range(signal_length // 2)]    # Convert to one-sided frequency range

    # FFT Computation and Range
    Y = fft(y)
    Y = Y[range(signal_length // 2)]

    return (frq, abs(Y))

def sample(rec, rate=44100, numframes=None):
    """
    Given a `SoundCard` recorder, get an audio sample and then compute
    the FFT of that sample.  

    :param rec: Audio device opened using `SoundCard`
    
    :param rate: Rate at which to sample the audio device
    :type rate: int

    :param numframes: Number of audio frames to wait for
    :type numframes: int

    :returns: A tuple of the frequency range and a list of channel data lists
    :rtype: tuple(int, list[list[float]])
    """
    data = rec.record(numframes=None)
    frq, chans = get_spectrum(data, rate)

    channels = map(list, zip(*chans))
    return (frq, [c for c in channels])

def samplegen(rec, rate=44100, numframes=None):
    while True:
        yield sample(rec, rate, numframes)

