import math, sys, time

from asciimatics.screen import Screen, ManagedScreen
from asciimatics.exceptions import ResizeScreenError


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
        self._old_data = None

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

        # "frequencies" is the "x" that we want to plot, and
        # term_width is the number of columns available.
        stepsize = len(frequencies) // term_width

        buckets = []
        for bucket in range(term_width):
            vals = []
            for channel in channel_data:
                for val in range(bucket * stepsize, (bucket+1) * stepsize):
                    vals.append(channel[val])

            # need math.fsum() since they are floating point values !!
            # also need to normalize to screen height so we can print.
            val_sum = (math.fsum([(0 + (term_height - 0)*v) for v in vals])) if len(vals) > 0 else 0
            buckets.append( int(min(term_height, val_sum)) )

        for x, bheight in enumerate(buckets):
            if bheight > 0:
                if self._old_data and len(self._old_data) == len(buckets):
                    old_height = self._old_data[x]

                    if old_height < bheight:
                        # Draw chars back from old height to new height
                        self._screen.move(x, term_height - old_height + 1)
                        self._screen.draw(x, term_height, char=self._char)
                    elif old_height > bheight:
                        # Erase characters back to the new height
                        self._screen.move(x, 0)
                        self._screen.draw(x, term_height - bheight - 1, char=" ")
                else:
                    # Draw a whole line
                    self._screen.move(x, term_height - bheight)
                    self._screen.draw(x, term_height, char=self._char)
                

        self._old_data = buckets
        self._screen.refresh()

    def start_render_loop(self):
        while True:
            try:
                with ManagedScreen() as screen:
                    while True:
                        self.render(screen=screen)
                        #time.sleep(0.008)
            except ResizeScreenError as e:
                continue
            except Exception as e:
                print(e)
                sys.exit(0)

