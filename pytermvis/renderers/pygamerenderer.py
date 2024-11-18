import math
import time

import numpy as np
import pygame

from pytermvis.common.common import (
    bin_fft,
    bin_signal,
    gamma_bin_fft,
    get_fft,
    remap,
)
from pytermvis.common.constants import MODE


COLORS = [ (255, 0, 0), (0, 255, 0), (0, 0, 255) ]


class PygameRenderer(object):

    def __init__(self, rate, period, sample_generator, mode, char="*"):
        self._rate = rate
        self._period = period
        self._sgen = sample_generator
        self._mode = mode
        self._char = char
        self._screen = None
        self._max = 1

    def _render(self):
        sample = np.mean(next(self._sgen), axis=1)

        screen_width, screen_height = pygame.display.get_surface().get_size()

        self._screen.fill((0,0,0,))

        num_bins = screen_width

        if self._mode == MODE.AUDIO:
            xs = np.arange(len(sample))
            ys = sample
        elif self._mode in [MODE.FFT, MODE.BFFT, MODE.GFFT]:
            fftfreqs, fft = get_fft(sample, self._rate)
            frequencies = fftfreqs[:self._period//2]
            magnitudes = np.abs(fft[:self._period//2])**2

            if self._mode == MODE.FFT:
                xs = frequencies
                ys = magnitudes
                self._max = np.max(ys)
                ys = ys / self._max
            elif self._mode == MODE.BFFT:
                num_bins = 20
                xs = np.arange(num_bins)
                ys = np.array(bin_fft(frequencies, magnitudes, num_bins))
                self._max = np.max(ys)
                ys = ys / self._max
            elif self._mode == MODE.GFFT:
                num_bins = 20
                xs=np.arange(num_bins)
                _, ys = gamma_bin_fft(
                    frequencies,
                    magnitudes,
                    self._rate,
                    num_bins,
                    gamma=2.0
                )
        else:
            raise NotImplementedError(
                "Mode {} not implemented".format(self._mode)
            )

        # Remap the values onto the screen's dimensions
        # (pygame coordinates have 0,0 in the top-left of the screen)
        xmi = np.min(xs)
        xmx = np.max(xs)
        xs = np.array([remap(x, xmi, xmx, screen_width*0.1, screen_width*0.9) for x in xs])

        ymi = np.min(ys)
        ymx = np.max(ys)
        ys = np.array([remap(y, ymi, ymx, screen_height*0.9, screen_height*0.1) for y in ys])

        points = list(zip(xs, ys))

        # draw on screen
        
        # draw points/one line
        #pygame.draw.lines(
        #    self._screen,
        #    COLORS[0],
        #    False,
        #    points,
        #)

        # draw lines/"bars"
        #for p in points:
        #    pygame.draw.line(
        #        self._screen,
        #        COLORS[0],
        #        (p[0], screen_height),
        #        p,
        #        2
        #    )

        # draw circles at each point
        for p in points:
            pygame.draw.circle(
                self._screen,
                COLORS[0],
                p,
                1,
            )

        pygame.display.flip()


    def start_render_loop(self):
        pygame.init()
        self._screen = pygame.display.set_mode((480,320), pygame.RESIZABLE)

        #clock = pygame.time.Clock()

        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode((event.w, event.h), pygame.DOUBLEBUF | pygame.RESIZABLE)

            self._render()
            #clock.tick(560)
