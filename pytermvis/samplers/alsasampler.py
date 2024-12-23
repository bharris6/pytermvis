import alsaaudio
import numpy as np

from sampler import Sampler


class AlsaSampler(Sampler):
    def __init__(
        self,
        rate=44100,
        period=1024,
        channels=2,
        aformat=alsaaudio.PCM_FORMAT_S16_LE,
        cardindex=-1,
        *args,
        **kwargs
    ):
        Sampler.__init__(self, rate=rate, period=period, *args, **kwargs)
        self._channels = channels
        self._format = aformat
        self._cardindex = cardindex

        # Found out which card to use from user
        cards = alsaaudio.cards()
        for i, c in enumerate(cards):
            print("{}: {}".format(i, c))
        card = int(input("Please choose a card from the choices above: "))

        self._cardindex = card

        # Instantiate our alsaaudio PCM
        self._inp = alsaaudio.PCM(
            alsaaudio.PCM_CAPTURE,
            alsaaudio.PCM_NORMAL,
            cardindex=self._cardindex,
        )

        # Set some values on our new capture PCM
        self._inp.setchannels(self.channels)
        self._inp.setrate(self._rate)
        self._inp.setformat(self._format)
        self._inp.setperiodsize(self._period)

    def sample(self):
        while True:
            try:
                l, data = self._inp.read()
            except TypeError:
                yield []

            if l > 0 and len(data) > 0:
                # TODO: enable different formats?
                # Right now, just signed int16s, little-endian...
                raw_sample = np.frombuffer(data, dtype="<i2")

                # A frame is an array of one sample per channel
                frames = np.reshape(raw_sample, [-1, self._channels])

                # Convert it to an array of floats
                float_frames = np.asarray(frames, dtype="float32") / 32767

                yield float_frames
