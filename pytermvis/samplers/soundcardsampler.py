import threading

import soundcard as sc

import numpy as np

from pytermvis.samplers.sampler import Sampler
from pytermvis.common import common

class SoundcardSampler(Sampler, threading.Thread):
    def __init__(self, rate=44100, period=1024):
        threading.Thread.__init__(self)
        self.daemon = True
        self._s_lock = threading.Lock()

        Sampler.__init__(self, rate, period)
        
        # Query for which card/device to use
        selections = sc.all_microphones(include_loopback=True)
        for i, s in enumerate(selections):
            print("{}: {}".format(i, s))

        dev = int( input("Please enter the number of the device to use: ") )
        dev_name = selections[dev].name

        # Instantiate our Soundcard mixin
        self._mixin = sc.get_microphone(id=dev_name, include_loopback=True) 

    def run(self):
        with self._mixin.recorder(samplerate=self._rate) as rec:
            while True:
                frames = rec.record(numframes=self._period)
                frq, chans = common.get_spectrum(frames, self._rate)
                with self._s_lock:
                    self._ffts.append((frq,chans))
    
    def _sample(self):
        # Return the average of all the collected ffts
        with self._s_lock:
            fft_list = list(self._ffts)

        frqs, ffts = [[x for x,y in fft_list], [y for x,y in fft_list]]

        if len(ffts) == 0 or len(frqs) == 0:
            return ([0], [[0]])
        else:
            frq = frqs[0]
        fft_mean = np.mean(ffts, 0)

        channels = map(list, zip(*fft_mean))
        channels = [c for c in channels]

        return (frq, channels)
