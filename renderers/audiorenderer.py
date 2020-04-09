from asciimatics.renderers import DynamicRenderer

import math
import soundcard as sc
import numpy as np
from scipy.fft import fft

def normalize(lower, upper, vals):
    return [(lower + (upper-lower)*v) for v in vals]

def get_spectrum(y, Fs):
    n = len(y)
    k = np.arange(n)
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
        

class AudioRenderer(DynamicRenderer):

    def __init__(self, channel_data, height, width, *args, **kwargs):
        super(AudioRenderer, self).__init__(height, width, *args, **kwargs)
        self._channel_data = channel_data

    def set_chan_data(self, channel_data):
        self._channel_data = channel_data

    def _write_line(self, x1, y1, x2, y2, char="*"):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self._write(char, x, y)
    
    def _render_now(self):
        #self._clear()

        # For each channel in channel_data, pull out the data and
        # write characters to the screen
        stepsize = len(self._channel_data[0]) // self._width

        buckets = []
        for bucket in range(self._width):
            vals = []
            for channel in self._channel_data:
                for val in range(bucket * stepsize, (bucket+1) * stepsize):
                    vals.append(channel[val])

            val_sum = (math.fsum(normalize(0, self._height, vals))) if \
                        len(vals) > 0 else 0

            buckets.append( int( min(self._height, val_sum) ) )

        for x, bheight in enumerate(buckets):
            if bheight > 0:
                self._write_line(x, self._height, x, self._height - bheight)
        
        return self._plain_image, self._colour_map


if __name__ == '__main__':
    
    import random, time
    from asciimatics.screen import Screen, ManagedScreen

    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{} : {}".format(i, s))

    s = int( input("Speaker Choice: ") )
    s_name = selections[s].name

    mixin = sc.get_microphone(id=s_name, include_loopback=True)
    
    with mixin.recorder(samplerate=44100) as rec:
        with ManagedScreen() as screen:

            height, width = screen.dimensions
            renderer = AudioRenderer([[],[]], height, width)

            while not screen.has_resized():
                frq, channel_data = sample(rec)
                renderer.set_chan_data(channel_data)
                text, cmap = renderer.rendered_text
                print("{}".format(text))
                #print("Length of rendered text: {}".format(len(text)))
                time.sleep(2)
