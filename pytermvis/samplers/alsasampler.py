import alsaaudio

import numpy as np

from pytermvis.samplers.sampler import Sampler
from pytermvis.common import common


class AlsaSampler(Sampler):
    def __init__(self, rate=44100, period=1024, channels=2, aformat=alsaaudio.PCM_FORMAT_S16_LE, cardindex=-1):
        Sampler.__init__(self, rate=rate, period=period)
        self._channels = channels
        self._format = aformat
        self._cardindex = cardindex
        
        # Instantiate our alsaaudio PCM
        self._inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, cardindex=self._cardindex) 

        # Set some values on our new capture PCM
        self._inp.setchannels(self._channels)
        self._inp.setrate(self._rate)
        self._inp.setformat(self._format)
        self._inp.setperiodsize(self._period)

    def _sample(self):
        try:
            l, data = self._inp.read()
        except TypeError:
            return ([0], [[0]])
            
        if l > 0 and len(data) > 0:
                
            # TODO: Enable different formats?
            # Right now, just signed int16s, little-endian
            raw_sample = np.frombuffer(data, dtype="<i2")

            # A frame is an array of one sample per channel
            frames = np.reshape(raw_sample, [-1, self._channels])

            # Convert it to an array of floats in range [-1,1]
            float_frames = np.asarray(frames / 32767, dtype="float32")

            frq, chans = common.get_spectrum(float_frames, self._rate)

            channels = map(list, zip(*chans))
            return (frq, [c for c in channels])

        else:
            return ([0], [[0]])
