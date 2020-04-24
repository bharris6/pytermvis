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
        
        # soundcard returns samples in float32, range [-1,1]
        # stackoverflow.com/questions/52020571/wasapi-shared-mode-what-amplitude-does-the-audio-engine-expect
        # frames * 0x7fffffff (seven f's) or frames * (1<<(32-1)) - 1)
        frq, chans = common.get_spectrum(frames, self._rate)
        
        channels = map(list, zip(*chans))
        return (frq, [c for c in channels])
