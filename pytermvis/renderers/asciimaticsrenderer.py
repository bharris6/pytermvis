import math, sys, time

import numpy as np

from asciimatics.screen import Screen, ManagedScreen
from asciimatics.exceptions import ResizeScreenError

from pytermvis.common import common


class AsciimaticsRenderer(object):

    def __init__(self, rgen, char="*"):
        """
        :param screen: Asciimatics Screen instance representing surface
        :type screen: asciimatics.screen.Screen

        :param rgen: Generator that yields audio samples to draw
        :type rgen: generator function

        :param char: Character to use when drawing
        :type char: Single-character string
        """
        self._screen = None
        self._rgen = rgen
        self._char = char
        self._old_data = []

    def render(self, screen):
        self._screen = screen

        # Since we are using a horizontal graph (bars go vertical)...
        #  --> term_width is the number of buckets
        #  --> term_height is the max amplitude for a bucket
        frequencies, channel_data = next(self._rgen)

        if len(frequencies) < 2:
            return

        if self._screen.has_resized():
            raise ResizeScreenError(message="Resized Screen")

        term_width = self._screen.width
        term_height = self._screen.height

        channel_sums = np.array(list(map(np.sum, zip(*channel_data))))
        channel_sums_binned = common.to_bins(channel_sums, term_width)

        for x, bheight in enumerate(channel_sums_binned):
            if len(self._old_data) > 0:
                old_height = self._old_data[x]
                old_fallof = int(old_height - 1)  # falloff each iteration should always be at least 1

                new_height = max(old_fallof, bheight) # account for fallof before comparison

                if old_height < new_height:
                    # draw from old height to new height
                    self._screen.move(x, term_height - term_height*old_height)
                    self._screen.draw(x, term_height - term_height*new_height, char=self._char)
                else:
                    # erase from old height to new height
                    self._screen.move(x, term_height - term_height*old_height)
                    self._screen.draw(x, term_height - term_height*new_height, char=" ")

            elif bheight > 0.001:
                # Draw a whole line
                self._screen.move(x, 0)
                self._screen.draw(x, term_height - term_height*bheight, char=" ")
                self._screen.move(x, term_height - term_height*bheight)
                self._screen.draw(x, term_height, char=self._char)
            else:
                self._screen.move(x, 0)
                self._screen.draw(x, term_height, char=" ")
                
        self._old_data = channel_sums_binned
        self._screen.refresh()

    def start_render_loop(self):
        while True:
            try:
                with ManagedScreen() as screen:
                    while True:
                        self.render(screen=screen)
                        time.sleep(0.008)
            except ResizeScreenError as e:
                continue
            except Exception as e:
                print(e)
                sys.exit(0)

