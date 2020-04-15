import numpy as np

from pytermvis.common import common


class Sampler(object):
    def __init__(self, rate=44100, period=1024):
        self._rate = rate
        self._period = period

    def samplegen(self):
        while True:
            yield self._sample()

    def _sample(self):
        # override
        pass

