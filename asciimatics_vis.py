import argparse, math, os, sys, time

from asciimatics.screen import Screen, ManagedScreen
from asciimatics.exceptions import ResizeScreenError

import numpy as np

from scipy.fft import fft

import soundcard as sc

SAMPLERATE = 44100

CHARACTER="*"


def normalize(lower, upper, vals):
    """ 
    Normalize all values so that they're between the lower
    and the upper bounds passed in.
    """
    return [(lower + (upper - lower)*v) for v in vals]
    # First, normalize to [0,1]
    m = min(vals)
    range = max(vals) - m
    norm_01 = (vals - m) / range
    
    # Now, normalize to [lower, upper]
    range = upper - lower
    normalized = (norm_01 * range) + lower
    return normalized
    
def get_spectrum(y, Fs):
    n = len(y)  # Length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T   # two sides frequency range
    frq = frq[range(n//2)]   # One side frequency range
    
    #Y = fft(y)//n # FFT Computation and Normalization
    Y = fft(y)
        
    Y = Y[range(n//2)]
    
    return (frq, abs(Y))

def sample(rec):
    data = rec.record(numframes=None)
    x, y = get_spectrum(data, SAMPLERATE)
    channels = map(list, zip(*y))
    return (x, [c for c in channels])
    
def display_loop(screen, rec, char):
    # Since we are using a horizontal graph (bars go vertical)...
    # term_width is the number of buckets to get
    # term_height is the maximum amplitude/value for a bucket
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
                
            # Now we want to normalize all those values to between 0 and the maximum we can print 
            # And then sum them up
            val_sum = (math.fsum( normalize(0, term_height, vals) )) if len(vals) > 0 else 0
            buckets.append(int(min(term_height, val_sum)))

        for x, bheight in enumerate(buckets):
            if bheight > 0:
                if old_values:
                
                    old_height = old_values[x]
                    
                    if old_height < bheight:
                        # Draw characters back from old height to new height
                        screen.move(x, term_height - old_height + 1)
                        screen.draw(x, term_height, char=char)
                    elif old_height > bheight:
                        # Erase characters back to the new height
                        #screen.move(x, term_height - old_height)
                        screen.move(x, 0)
                        screen.draw(x, term_height - bheight - 1, char=" ")
                else:
                    # Draw entire line
                    #screen.move(x, 0)
                    #screen.draw(x, term_height - bheight, char=" ")
                    
                    screen.move(x, term_height - bheight)
                    screen.draw(x, term_height, char=char)
                    
                
        screen.refresh()
        old_values = buckets
        
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Python Terminal Visualizer")

    parser.add_argument("-c", "--char", action="store", dest="char", default=CHARACTER)

    parser_args = parser.parse_args()
    
    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{}: {}".format(i, s))
        
    speaker_choice = int(input("Please enter the number of the speakers you want to use> "))
    speaker_name = selections[speaker_choice].name
    
    mixin = sc.get_microphone(id=speaker_name, include_loopback=True)

    with mixin.recorder(samplerate=SAMPLERATE) as rec:
        while True:
            try:
                #Screen.wrapper(display_loop, arguments=[rec])
                with ManagedScreen() as screen:
                    display_loop(screen, rec, parser_args.char)
            except ResizeScreenError as e:
                continue
            except Exception as e:
                print("Exception:\n{}".format(e))
                sys.exit(0)
            
