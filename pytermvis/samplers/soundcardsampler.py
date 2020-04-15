import soundcard as sc

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
        #self._rec = self._mixin.recorder(samplerate=self._rate)

    def _sample(self):
        frames = self._mixin.record(samplerate=self._rate, numframes=self._period)
        frq, chans = common.get_spectrum(frames, self._rate)

        channels = map(list, zip(*chans))
        return (frq, [c for c in channels])
