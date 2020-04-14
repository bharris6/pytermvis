import os, shutil, time

import numpy as np

from scipy.fft import fft
from scipy import interpolate


def remap(x, x1, x2, y1, y2):
    if (x2 == x1 and x2 == 0) or (y2 == y1 and y2 == 0):
        return 0
    return (((x - x1) * (y2 - y1)) / (x2 - x1)) + y1

def to_bins(ar, b):
    """ ar is array of values, b is number of buckets """
    a = len(ar)
    n = int(a / b)

    if b <= a:
        bins = []
        for i in range(0, b):
            arr = []
            for j in range(i * n, (i+1)*n):
                if j >= a:
                    break
                arr.append(ar[j])
            bins.append(np.sum(arr))
        return bins
    else:
        # number of buckets is bigger than array, need to
        # interpolate those values...

        # This is using numpy, uses only linear interpolation
        #return np.interp(np.arange(b), np.arange(a), ar)

        # This is using scipy, which uses a better interpolation method
        f = interpolate.interp1d(np.arange(a), ar, fill_value="extrapolate")
        return f(np.arange(b))
        

class AudioRenderer(object):

    def __init__(self, rgen, char="*", *args, **kwargs):
        self._rgen = rgen
        self._channel_data = None
        self._char = char

    def _render_once(self):
        
        frq, channel_data = next(self._rgen)

        term_width, term_height = shutil.get_terminal_size()

        # Can only draw as many frequencies as there are lines
        # in the terminal...
        num_frequencies = len(frq)
        if num_frequencies > term_height:
            num_buckets = term_height
            stepsize = num_frequencies // num_buckets
        else:
            num_buckets = len(frq)
            stepsize = term_height // num_buckets

        buckets = []
        for c in channel_data:
            carray = np.asarray(c)
            cbuckets = np.split(carray, range(0, len(c), stepsize))
            csums = [(term_width*cb.sum())//stepsize for cb in cbuckets]
            buckets.append(csums)

        bucketsums = list(map(np.sum, zip(*buckets)))
        #print("Buckets: {}\n -- bucketsums: {}".format(buckets, bucketsums))

        mi = min(bucketsums)
        mx = max(bucketsums)

        os.system("cls||clear")
        for x, y in enumerate(bucketsums):
            ys = remap(y, mi, mx, 0, term_width)
            #print("Frequency: {}, Amplitude: {}".format(frq[x], y))
            print("{}".format(self._char)*int(ys))

        
    def _render_other(self):
        
        frq, channel_data = next(self._rgen)

        if len(frq) < 100:
            return

        term_width, term_height = shutil.get_terminal_size()

        # Can only draw as many frequencies as there are columns
        # in the terminal...
        num_buckets = term_width

        # First, compute all the channel sums
        low_freq_cutoff = 3
        high_freq_cutoff = 22050

        frequencies = []
        channels = [[] for c in range(len(channel_data))]
        for fx, f in enumerate(frq):
            if f > low_freq_cutoff and f < high_freq_cutoff:
                frequencies.append(f)
                for c in range(len(channel_data)):
                    channels[c].append(channel_data[c][fx])

        channel_sums = np.array(list(map(np.sum, zip(*channels))))

        # Now need to aggregate the channel sums into the number of columns available
        channel_sums_binned = to_bins(channel_sums, term_width)

        # And then make sure they fit on-screen
        mi = min(channel_sums_binned)
        mx = max(channel_sums_binned)
        channel_sums_binned = np.array([ remap(cs, mi, mx, 0, term_height) for cs in channel_sums_binned] )

        lines = []
        for l in range(0, term_height):
            lines.append("".join(["{}".format(self._char) if t else " " for t in channel_sums_binned >= l ]))

        os.system("cls||clear")
        lines.reverse()
        for l in lines:
            print(l)


    def start_render_loop(self):
        while True:
            self._render_other()
            time.sleep(0.033)

if __name__ == '__main__':

    import soundcard as sc

    from ..common import samplegen

    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{} : {}".format(i, s))

    s = int( input("Speaker Choice: ") )
    s_name = selections[s].name

    mixin = sc.get_microphone(id=s_name, include_loopback=True)
    
    with mixin.recorder(samplerate=44100) as rec:
        ar = AudioRenderer(samplegen(rec), char="|")
        ar.start_render_loop()
        
