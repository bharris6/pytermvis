from asciimatics.renderers import DynamicRenderer

import math, sys, os
import soundcard as sc
import numpy as np
from scipy.fft import fft

def normalize(lower, upper, vals):
    return [(lower + (upper-lower)*v) for v in vals]

def get_spectrum(y, Fs):
    n = len(y)
    k = np.arange(n)
    T = n / Fs
    frq = k / T
    frq = frq[range(n // 2)]
    Y = fft(y)
    Y = Y[range(n // 2)]

    return (frq, abs(Y))

def sample(rec):
    data = rec.record(numframes=None)
    frq, chans = get_spectrum(data, 44100)
    channels = map(list, zip(*chans))
    return (frq, [c for c in channels])
        

class AudioRenderer(DynamicRenderer):

    def __init__(self, recorder, height, width, *args, **kwargs):
        super(AudioRenderer, self).__init__(height, width, *args, **kwargs)
        self._rec = recorder
        self._channel_data = None

    def _sample(self):
        data = self._rec.record(numframes=None)
        frq, chans = get_spectrum(data, 44100)
        channels = map(list, zip(*chans))
        return(frq, [c for c in channels])

    def _render_now(self):
        
        frq, channel_data = self._sample()

        term_width = self._width
        term_height = self._height

        stepsize = len(frq) // term_width

        buckets = []
        for bucket in range(term_width):
            vals = []
            for channel in channel_data:
                for val in range(bucket * stepsize, (bucket+1) * stepsize):
                    vals.append(channel[val])

            val_sum = (math.fsum(normalize(0, term_height, vals))) if len(vals) > 0 else 0
            buckets.append( int( min(term_height, val_sum) ) )

        for x, bheight in enumerate(buckets):
            if self._channel_data:
                old_height = self._channel_data[x]
    
                if old_height < bheight:
                    # Draw from old height to new height
                    for y in range(bheight, old_height):
                        self._write("*", x, y)
                elif old_height > bheight:
                    # Erase from old height to new height
                    for y in range(old_height, bheight):
                        self._write(" ", x, y)
            else:
                for y in range(term_height-bheight, term_height):
                    self._write("*", x, y)

        #self._channel_data = buckets

        return self._plain_image, self._colour_map


if __name__ == '__main__':
    
    import random, time
    from asciimatics.screen import Screen
    from asciimatics.effects import Print
    from asciimatics.scene import Scene
    from asciimatics.exceptions import ResizeScreenError

    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{} : {}".format(i, s))

    s = int( input("Speaker Choice: ") )
    s_name = selections[s].name

    mixin = sc.get_microphone(id=s_name, include_loopback=True)
    
    with mixin.recorder(samplerate=44100) as rec:

        def demo(screen):
            scenes = []
            effects = [ Print(screen, AudioRenderer(rec, screen.height, screen.width), x=0, y=0, transparent=False) ]
            scenes.append(Scene(effects, -1))
            #screen.play(scenes, stop_on_resize=True)
            screen.set_scenes(scenes)
            while True:
                if screen.has_resized():
                    raise ResizeScreenError("Resized", scene=None)
                screen.draw_next_frame(repeat=False)
                time.sleep(0.033)
            
        last_scene = None
        while True:
            try:
                Screen.wrapper(demo, catch_interrupt=True)
                sys.exit(0)
            except ResizeScreenError as e:
                continue
