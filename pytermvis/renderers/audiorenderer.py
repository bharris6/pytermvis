import os, shutil, time

import numpy as np

from scipy.fft import fft

from pytermvis.common import common

if os.name == 'nt':
    screen_clear = "cls"
else:
    screen_clear = "clear"

class AudioRenderer(object):

    def __init__(self, rgen, char="*", vtype="graph", *args, **kwargs):
        self._rgen = rgen
        self._channel_data = None
        self._char = char
        self._vtype = vtype

    def _render(self):
        
        frq, channel_data = next(self._rgen)

        if len(frq) < 2:
            return

        term_width, term_height = shutil.get_terminal_size()

        # Can only draw as many frequencies as there are columns
        # in the terminal...
        num_buckets = term_width

        # First, compute all the channel sums
        channel_sums = np.array(list(map(np.sum, zip(*channel_data))))

        # Now need to aggregate the channel sums into the number of columns available
        channel_sums_binned = common.to_bins(channel_sums, term_width)

        ## And then make sure they fit on-screen
        channel_sums_binned = channel_sums_binned * term_height

        lines = []
        for l in range(0, term_height):
            if self._vtype == "graph":
                # Graph view, lines
                lines.append("".join(["{}".format(self._char) if t else " " for t in channel_sums_binned >= l ]))
            else:
                # Scope view, just discrete points
                # Points is an array of indices where the condition is True
                points = np.where(np.logical_and(channel_sums_binned >= l, channel_sums_binned < l+1))[0]
                lines.append("".join(["{}".format(self._char) if x in points else " " for x in range(term_width)]))
                

        os.system(screen_clear)
        lines.reverse()
        for l in lines:
            print(l)

    def start_render_loop(self):
        while True:
            self._render()
            time.sleep(0.01667)

if __name__ == '__main__':

    import soundcard as sc

    from ..common import samplegen

    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{} : {}".format(i, s))

    s = int( input("Speaker Choice: ") )
    s_name = selections[s].name

    mixin = sc.get_microphone(id=s_name, include_loopback=True)
    
    with mixin.recorder(samplerate=44100) as rec:
        ar = AudioRenderer(samplegen(rec), char="|")
        ar.start_render_loop()
        
