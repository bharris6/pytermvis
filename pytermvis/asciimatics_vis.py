import argparse, math, os, sys, time

from asciimatics.screen import Screen, ManagedScreen
from asciimatics.exceptions import ResizeScreenError

import numpy as np

from scipy.fft import fft

import soundcard as sc

from common import *

SAMPLERATE = 44100
CHARACTER="*"


def display_loop(screen, rec, char):
    """
    The loop which handles getting an audio sample, computing its
    frequency transformation, and then displaying the resulting 
    FFT data visually.

    :param screen: Asciimatics Screen representing the drawing surface
    :type screen: asciimatics.screen.Screen

    :param rec: SoundCard recording device to get audio samples from
    
    :param char: Character to use in the visualization display
    :type char: string -- one-character

    :raises asciimatics.exceptions.ResizeScreenError: Screen Resizing Event
    """
    # Since we are using a horizontal graph (bars go vertical)...
    #  --> term_width is the number of buckets to get
    #  --> term_height is the maximum amplitude/value for a bucket
    old_values = None
    while True:
        frq, channel_data = sample(rec)

        if screen.has_resized():
            screen.clear()
            raise ResizeScreenError(message="Screen has been resized")
        
        term_width = screen.width
        term_height = screen.height
        
        # frq is the "x" that we want to plot, and
        # term_width is the numbers of columns that are available
        # (i.e. how many buckets to use)
        stepsize = len(frq) // term_width
        
        buckets = []
        for bucket in range(term_width):
            vals = []
            for channel in channel_data:
                # need math.fsum() since they are floating point values !!
                for val in range(bucket*stepsize, (bucket+1)*stepsize):
                    vals.append(channel[val])
                
            # Now we want to normalize all those values to between 0 
            # and the maximum we can print, and then sum them up
            val_sum = (math.fsum(normalize(0, term_height, vals))) if len(vals) > 0 else 0
            buckets.append(int(min(term_height, val_sum)))

        for x, bheight in enumerate(buckets):
            if bheight > 0:
                if old_values:
                
                    old_height = old_values[x]
                    
                    if old_height < bheight:
                        # Draw characters back from old height to 
                        # new height
                        screen.move(x, term_height - old_height + 1)
                        screen.draw(x, term_height, char=char)
                    elif old_height > bheight:
                        # Erase characters back to the new height
                        #screen.move(x, term_height - old_height)
                        screen.move(x, 0)
                        screen.draw(x, term_height - bheight - 1, char=" ")
                else:
                    # Draw whole line
                    screen.move(x, term_height - bheight)
                    screen.draw(x, term_height, char=char)
                    
                
        screen.refresh()
        old_values = buckets
        
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="pytermvis -- Python Terminal Visualizer")

    parser.add_argument("-c", "--char", action="store", dest="char", default=CHARACTER)
    parser.add_argument("-s", "--sample-rate", action="store", dest="samplerate", default=SAMPLERATE)

    parser_args = parser.parse_args()

    SAMPLERATE = int(parser_args.samplerate)
    
    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{}: {}".format(i, s))
        
    speaker_choice = int(input("Please enter the number of the speakers you want to use> "))
    speaker_name = selections[speaker_choice].name
    
    mixin = sc.get_microphone(id=speaker_name, include_loopback=True)

    with mixin.recorder(samplerate=SAMPLERATE) as rec:
        while True:
            try:
                with ManagedScreen() as screen:
                    display_loop(screen, rec, parser_args.char)
            except ResizeScreenError as e:
                continue
            except Exception as e:
                print("Exception:\n{}".format(e))
                sys.exit(0)
            
