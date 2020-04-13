import fractions, math, sys, os, shutil, time
import soundcard as sc
import numpy as np
from scipy.fft import fft
from scipy import interpolate

def normalize(lower, upper, vals):
    return [(lower + (upper-lower)*v) for v in vals]

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
        f = interpolate.interp1d(np.arange(a), ar, fill_value="extrapolate")
        return f(np.arange(b))
        

def get_spectrum(y, Fs):
    n = len(y)
    k = np.arange(n)    # This is each frequency in Hz represented by FFT amplitudes
    T = n / Fs
    frq = k / T
    frq = frq[range(n // 2)]
    Y = fft(y)
    Y = Y[range(n // 2)]

    return (frq, abs(Y))

def sample(rec):
    data = rec.record(numframes=None)
    frq, chans = get_spectrum(data, 44100)
    channels = map(list, zip(*chans))
    return (frq, [c for c in channels])
        

class AudioRenderer(object):

    def __init__(self, recorder, *args, **kwargs):
        self._rec = recorder
        self._channel_data = None

    def _sample(self):
        data = self._rec.record(numframes=None)
        frq, chans = get_spectrum(data, 44100)
        channels = map(list, zip(*chans))
        return(frq, [c for c in channels])

    def _render_once(self):
        
        frq, channel_data = self._sample()

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

        #print("Term Height: {}, Len(frq): {}, nbuckets: {}, step: {}".format(term_height, len(frq), num_buckets, stepsize))

        os.system("cls||clear")
        for x, y in enumerate(bucketsums):
            ys = remap(y, mi, mx, 0, term_width)
            #print("Frequency: {}, Amplitude: {}".format(frq[x], y))
            print("|"*int(ys))

        
    def _render_other(self):
        
        frq, channel_data = self._sample()

        if len(frq) < 200:
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
                for c, ch in enumerate(channel_data):
                    channels[c].append(ch)

        channel_sums = np.array(list(map(np.sum, zip(*channel_data))))

        # Now need to aggregate the channel sums into the number of columns available
        channel_sums_binned = to_bins(channel_sums, term_width)

        # And then make sure they fit on-screen
        mi = min(channel_sums_binned)
        mx = max(channel_sums_binned)
        channel_sums_binned = np.array([ remap(cs, mi, mx, 0, term_height) for cs in channel_sums_binned] )

        lines = []
        for l in range(0, term_height):
            lines.append("".join(["#" if t else " " for t in channel_sums_binned >= l ]))

        os.system("cls||clear")
        lines.reverse()
        for l in lines:
            print(l)

if __name__ == '__main__':
    
    import random, time
    from asciimatics.screen import Screen
    from asciimatics.effects import Print
    from asciimatics.scene import Scene
    from asciimatics.exceptions import ResizeScreenError

    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{} : {}".format(i, s))

    s = int( input("Speaker Choice: ") )
    s_name = selections[s].name

    mixin = sc.get_microphone(id=s_name, include_loopback=True)
    
    with mixin.recorder(samplerate=44100) as rec:
        ar = AudioRenderer(rec)

        while True:
            #ar._render_once()
            ar._render_other()
            time.sleep(0.033)
