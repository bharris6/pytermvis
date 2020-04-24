import soundcard as sc

import numpy as np

from pytermvis.samplers.sampler import Sampler
from pytermvis.common import common

class SoundcardSampler(Sampler):
    def __init__(self, rate=44100, period=1024):
        Sampler.__init__(self, rate, period)
        
        # Query for which card/device to use
        selections = sc.all_speakers()
        for i, s in enumerate(selections):
            print("{}: {}".format(i, s))

        dev = int( input("Please enter the number of the device to use: ") )
        dev_name = selections[dev].name

        # Instantiate our Soundcard mixin
        self._mixin = sc.get_microphone(id=dev_name, include_loopback=True) 

    def _sample(self):
        frames = self._mixin.record(samplerate=self._rate, numframes=self._period)
        
        # soundcard returns samples in an array of frames x channels type of float32, range [-1,1]
        frq, chans = common.get_spectrum(frames, self._rate)
        self._ffts.append(chans)

        # Return the average of all the collected ffts
        ffts = list(self._ffts)
        fft_mean = np.mean(ffts, 0)

        channels = map(list, zip(*fft_mean))
        channels = [c for c in channels]
        
        return (frq, channels)
