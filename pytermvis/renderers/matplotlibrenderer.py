import matplotlib.pyplot as plt
import numpy as np

from pytermvis.common.common import (
    bin_fft,
    gamma_bin_fft,
    get_fft,
)
from pytermvis.common.constants import MODE


class MatplotlibRenderer(object):

    def __init__(self, rate, period, sample_generator, mode, bins=20):
        self._rate = rate
        self._period = period
        self._sgen = sample_generator
        self._mode = mode
        self._num_bins = bins
        self._fftmax = 1

        self._fig, (self._ax) = plt.subplots(1)

        if self._mode == MODE.AUDIO:
            self._xvals = np.arange(0, 2*period, 2)
            self._line, = self._ax.plot(self._xvals, np.random.rand(period))
            self._ax.set_ylim(-1, 1)
            self._ax.set_xlim(0, 2*period)
            self._ax.set_axis_off()
        elif self._mode == MODE.FFT:
            self._xvals = np.linspace(0, rate//2, period//2)
            self._line, = self._ax.semilogx(
                self._xvals,
                np.random.rand(period//2),
            )
            self._ax.set_xlim(0, rate/2)
            self._ax.set_ylim(0, 1)
            self._ax.set_axis_off()
        elif self._mode == MODE.BFFT or self._mode == MODE.GFFT:
            self._xvals = np.arange(0, self._num_bins, 1)
            self._line, = self._ax.plot(
                self._xvals,
                np.random.rand(self._num_bins),
                linestyle="None",
                marker="o",
            )
            self._ax.set_xlim(-1, self._num_bins+1)
            self._ax.set_ylim(-.01, .1)
            self._ax.set_axis_off()
        else:
            raise NotImplementedError(
                "Renderer mode {} not implemented.".format(mode)
            )

    def _render(self):
        sample = next(self._sgen)
        sample = np.mean(sample, axis=1)
        if self._mode == MODE.AUDIO:
            self._line.set_ydata(sample)  # just the first channel
        else:
            fftfreqs, fft = get_fft(sample, self._rate)
            frequencies = fftfreqs[:self._period//2]
            magnitudes = np.abs(fft[:self._period//2])**2

            if self._mode == MODE.FFT:
                self._fftmax = max(self._fftmax, np.max(magnitudes))
                self._line.set_data(frequencies, magnitudes/self._fftmax)

            elif self._mode == MODE.BFFT:
                binned_fft = bin_fft(frequencies, magnitudes, self._num_bins)
                binned_fft = binned_fft[:len(self._xvals)]
                self._fftmax = max(self._fftmax, np.max(binned_fft))
                self._line.set_ydata(binned_fft/self._fftmax)

            elif self._mode == MODE.GFFT:
                _, gfft = gamma_bin_fft(
                    frequencies,
                    magnitudes,
                    self._rate,
                    self._num_bins,
                    gamma=2.0
                )
                self._fftmax = max(self._fftmax, np.max(gfft))
                self._line.set_data(self._xvals[:len(gfft)], gfft)

        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

    def start_render_loop(self):
        plt.show(block=False)

        while True:
            self._render()
