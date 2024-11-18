from pytermvis.common.constants import SAMPLER


class Sampler(object):
    def __init__(self, rate=44100, period=1024):
        self._rate = rate
        self._period = period

    def sample(self):
        # override this method
        while True:
            yield []

    @staticmethod
    def get_sampler(sample_type=None, *args, **kwargs):
        if sample_type == SAMPLER.SOUNDCARD:
            from .soundcardsampler import SoundcardSampler
            return SoundcardSampler(*args, **kwargs)
        else:
            raise ValueError("Sampler {} not implemented.".format(sample_type))
