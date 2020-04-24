import os, shutil, time

import numpy as np

from scipy.fft import fft

from pytermvis.common import common

if os.name == 'nt':
    screen_clear = "cls"
else:
    screen_clear = "clear"

class AudioRenderer(object):

    def __init__(self, rgen, char="*", *args, **kwargs):
        self._rgen = rgen
        self._channel_data = None
        self._char = char

    def _render_once(self):
        
        frq, channel_data = next(self._rgen)
        if len(frq) < 2:
            return

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

        mi = min(bucketsums)
        mx = max(bucketsums)

        #os.system("cls||clear")
        os.system(screen_clear)
        for x, y in enumerate(bucketsums):
            ys = common.remap(y, mi, mx, 0, term_width)
            #print("Frequency: {}, Amplitude: {}".format(frq[x], y))
            print("{}".format(self._char)*int(ys))

        
    def _render_other(self):
        
        frq, channel_data = next(self._rgen)

        if len(frq) < 2:
            return

        term_width, term_height = shutil.get_terminal_size()

        # Can only draw as many frequencies as there are columns
        # in the terminal...
        num_buckets = term_width

        # First, compute all the channel sums
        channel_sums = np.array(list(map(np.sum, zip(*channel_data))))

        # Now need to aggregate the channel sums into the number of columns available
        channel_sums_binned = common.to_bins(channel_sums, term_width)

        ## And then make sure they fit on-screen
        channel_sums_binned = channel_sums_binned * term_height

        lines = []
        for l in range(0, term_height):
            lines.append("".join(["{}".format(self._char) if t else " " for t in channel_sums_binned >= l ]))

        #os.system("cls||clear")
        os.system(screen_clear)
        lines.reverse()
        for l in lines:
            print(l)

    def start_render_loop(self):
        while True:
            self._render_other()
            time.sleep(0.0167)

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
        
