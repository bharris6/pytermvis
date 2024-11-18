from enum import Enum


class vEnum(Enum):
    def __str__(self):
        return self.value


class SAMPLER(vEnum):
    SOUNDCARD = "soundcard"
    ALSAAUDIO = "alsaaudio"


class RENDERER(vEnum):
    ASCIIMATICS = "asciimatics"
    MATPLOTLIB = "matplotlib"
    TEXT = "text"


class MODE(vEnum):
    AUDIO = "audio"
    FFT = "fft"
    BFFT = "bfft"
    GFFT = "gfft"
