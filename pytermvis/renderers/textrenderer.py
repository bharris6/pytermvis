import os
import shutil
import time

import numpy as np

from pytermvis.common.common import (
    bin_fft,
    bin_signal,
    gamma_bin_fft,
    get_fft,
    remap,
)
from pytermvis.common.constants import MODE


if os.name == 'nt':
    screen_clear = 'cls'
else:
    screen_clear = 'clear'


class TextRenderer(object):

    def __init__(
        self, rate, period, sample_generator, mode, char="*"
    ):
        self._rate = rate
        self._period = period
        self._sgen = sample_generator
        self._mode = mode
        self._char = char

        self._fftmax = 1

    def _render(self):
        #sample = next(self._sgen)[:, 0]  # just the first channel
        sample = np.mean(next(self._sgen), axis=1)

        term_width, term_height = shutil.get_terminal_size()
        
        # Can only draw as many buckets/bins as there are columns in the
        # terminal/screen...
        num_bins = term_width

        if self._mode == MODE.AUDIO:
            vals = np.array(bin_signal(sample, num_bins))
        elif self._mode in [MODE.FFT, MODE.BFFT, MODE.GFFT]:
            fftfreqs, fft = get_fft(sample, self._rate)
            frequencies = fftfreqs[:self._period//2]
            magnitudes = np.abs(fft[:self._period//2])**2

            if self._mode == MODE.FFT or self._mode == MODE.BFFT:
                vals = np.array(bin_fft(frequencies, magnitudes, num_bins))
            else:  # self._mode == MODE.GFFT:
                _, vals = gamma_bin_fft(
                    frequencies,
                    magnitudes,
                    self._rate,
                    num_bins,
                    gamma=2.0
                )
                vals = np.array([remap(v, np.min(vals), np.max(vals), 0, 1) for v in vals])
        else:
            raise NotImplementedError(
                "Mode {} not implemented.".format(self._mode)
            )
            
        # Scale the height to fit on the screen
        vals = vals * term_height

        lines = []
        for l in range(0, term_height):
            lines.append("".join(["{}".format(self._char) if t else " " for t in vals >= l ]))

        os.system(screen_clear)
        lines.reverse()
        for l in lines:
            print(l)


    def start_render_loop(self):
        while True:
            self._render()
            #time.sleep(0.01)
