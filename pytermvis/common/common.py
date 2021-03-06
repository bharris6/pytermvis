import numpy as np
from scipy.fft import fft
from scipy import interpolate 

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

def to_bins(ar, b, xvals=None):
    """
    Given an array ar, and number of buckets b, return a normalized
    set of bins (values in range [0,1])
    
    :param ar: Array to act on
    :type ar: Python list or numpy array
    
    :param b: Number of bins to sum over
    :type b: int

    :param xvals: Values to use as x values/coordinates for ar's "y values"
    :type xvals: array of numbers

    :returns: An array of bins that have values between 0 and 1
    :rtype: numpy array
    """
    a = len(ar)
    n = int(a / b)

    if b <= a:
        bins = []
        for i in range(0, b):
            arr = []
            for j in range(i*n, (i+1)*n):
                if j >= a:
                    break
                arr.append(ar[j])
            bins.append(np.sum(arr) / len(arr))
        bins = np.array(bins)
        mx = np.max(bins)
        return bins if mx == 0 else bins / mx
    else:
        # Number of buckets is bigger than array, need to 
        # interpolate those values.  

        # Using scipy, which has a better interpolation method
        if not xvals is None:
            f = interpolate.interp1d(xvals, ar, fill_value="extrapolate")
        else:
            f = interpolate.interp1d(np.arange(a), ar, fill_value="extrapolate")

        interpolated = f(np.arange(b))
        return interpolated / np.max(interpolated)
                
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
    Y = abs(Y[range(signal_length // 2)])

    # Now want to normalize the values to 0-1
    #Y = np.nan_to_num(Y / np.max(Y))
    Y = Y * 2 / (2 * (signal_length // 2))

    # And set tiny values to 0
    #Y[Y <= 0.001] = 0

    return (frq, Y)


