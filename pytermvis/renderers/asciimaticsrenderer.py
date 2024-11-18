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
        self._max = 1 

    def _render(self):

        #sample = next(self._sgen)[:, 0]  # just the first channel
        sample = np.mean(next(self._sgen), axis=1)

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

        if self._mode == MODE.AUDIO:
            xs = np.arange(term_width)
            ys = np.array(bin_signal(sample, term_width))
            self._max = np.max(ys)
            ys = ys / self._max
        elif self._mode in [MODE.FFT, MODE.BFFT, MODE.GFFT]:
            fftfreqs, fft = get_fft(sample, self._rate)
            frequencies = fftfreqs[:self._period//2]
            magnitudes = np.abs(fft[:self._period//2])**2

            if self._mode == MODE.FFT:
                xs = np.arange(term_width)
                ys = np.array(bin_fft(frequencies, magnitudes, term_width))
                self._max = np.max(ys)
                ys = ys / self._max
            elif self._mode == MODE.BFFT:
                num_bins = 20
                xs = np.arange(num_bins)
                ys = np.array(bin_fft(frequencies, magnitudes, num_bins))
                self._max = np.max(ys)
                ys = ys / self._max
            else:  # self._mode == MODE.GFFT:
                num_bins = 20
                xs = np.arange(num_bins)
                _, ys = gamma_bin_fft(
                    frequencies,
                    magnitudes,
                    self._rate,
                    num_bins,
                    gamma=2.0,
                )

            ys = np.array(
                [remap(y, np.min(ys), np.max(ys), 0, 1) for y in ys]
            )

        else:
            raise NotImplementedError(
                "Mode {} not implemented".format(self._mode)
            )

        # Scale the bin edges to fit on the screen
        xmi = np.min(xs)
        xmx = np.max(xs)
        xs = np.array([remap(x, xmi, xmx, 0, term_width) for x in xs])

        # Scale the height to fit on the screen
        ymi = np.min(ys)
        ymx = np.max(ys)
        ys = np.array([remap(y, ymi, ymx, 0, term_height) for y in ys])

        self._screen.clear()
        for x,y in zip(xs, ys):
            # graph, print bars
            self._screen.move(x, term_height - int(y))
            self._screen.draw(x, term_height, char=self._char)

            # scope, print discrete points
            #self._screen.print_at(self._char, x, term_height - int(y))
 
        self._screen.refresh()

    def start_render_loop(self):
        while True:
            try:
                with ManagedScreen() as screen:
                    self._screen = screen
                    while True:
                        self._render()
                        #time.sleep(0.05)
            except ResizeScreenError as e:
                continue
            except Exception as e:
                print(e)
                sys.exit(0)

