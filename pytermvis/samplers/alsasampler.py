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

        # Find out which card to use from user
        cards = alsaaudio.cards()
        for i,c in enumerate(cards):
            print("{}: {}".format(i, c))
        card = int(input("Please choose a card from the above: "))

        self._cardindex = card
        
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
            return ([], [[]])
            
        if l > 0 and len(data) > 0:
                
            # TODO: Enable different formats?
            # Right now, just signed int16s, little-endian
            raw_sample = np.frombuffer(data, dtype="<i2")

            # A frame is an array of one sample per channel
            frames = np.reshape(raw_sample, [-1, self._channels])

            # Convert it to an array of floats
            float_frames = np.asarray(frames, dtype="float32")/32767

            frq, chans = common.get_spectrum(float_frames, self._rate)
            self._ffts.append(chans)

            # Return the average of all the collected ffts
            fft_mean = np.mean(list(self._ffts), 0)

            channels = map(list, zip(*fft_mean))
            channels = [c for c in channels]
            return (frq, channels)

        else:
            return ([], [[]])
