import math
import sys
import time

import numpy as np

from asciimatics.screen import Screen, ManagedScreen
from asciimatics.exceptions import ResizeScreenError

from pytermvis.common.common import (
    bin_fft,
    bin_signal,
    gamma_bin_fft,
    get_fft,
    remap,
)
from pytermvis.common.constants import MODE


class AsciimaticsRenderer(object):

    def __init__(self, rate, period, sample_generator, mode, char="*"):
        """
        :param sample_generator: Generator that yields audio samples to draw
        :type sample_generator: generator function

        :param char: Character to use when drawing
        :type char: Single-character string
        """
        self._rate = rate
        self._period = period
        self._sgen = sample_generator
        self._mode = mode
        self._char = char
        self._screen = None

    def _render(self):

        sample = next(self._sgen)[:, 0]  # just the first channel

        # Since we are using a horizontal graph (bars go vertical)...
        #  --> term_width is the number of buckets
        #  --> term_height is the max amplitude for a bucket
        if self._screen.has_resized():
            raise ResizeScreenError(message="Resized Screen")

        term_width = self._screen.width
        term_height = self._screen.height

        # Can only draw as many buckets/bins as there are columns in the
        # terminal/screen...
        num_bins = term_width

        #channel_sums = np.array(list(map(np.sum, zip(*channel_data))))
        #channel_sums_binned = common.to_bins(channel_sums, term_width)

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
                    gamma=2.0,
                )
                vals = np.array(
                    [remap(v, np.min(vals), np.max(vals), 0, 1) for v in vals]
                )
        else:
            raise NotImplementedError(
                "Mode {} not implemented".format(self._mode)
            )

        # Scale the height to fit on the screen
        vals = vals * term_height

        self._screen.clear()
        for x, bheight in enumerate(vals):
            # scope, print discrete points
            self._screen.print_at(self._char, x, term_height - int(bheight))
 
        self._screen.refresh()

    def start_render_loop(self):
        while True:
            try:
                with ManagedScreen() as screen:
                    self._screen = screen
                    while True:
                        self._render()
            except ResizeScreenError as e:
                continue
            except Exception as e:
                print(e)
                sys.exit(0)

