import math, os, sys, time

import pygame

import numpy as np

from scipy.fft import fft

import soundcard as sc

from common import *

SAMPLERATE = 44100
COLORS = [ (255, 0, 0), (0, 255, 0), (0, 0, 255) ]


def sample(rec):
    data = rec.record(numframes=None)
    x, y = get_spectrum(data, SAMPLERATE)
    channels = map(list, zip(*y))
    return (x, [c for c in channels])
    
def display_loop(screen, rec):
    # Since we are using a horizontal graph (bars go vertical)...
    # term_width is the number of buckets to get
    # term_height is the maximum amplitude/value for a bucket
    frq, channel_data = sample(rec)
    
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    # Want to adjust size to be a little less than fullscreen
    scale = 0.9
    term_width = scale * screen_width
    term_height = scale * screen_height
    
    num_buckets = 120
    
    # frq is the "x" that we want to plot
    stepsize = len(frq) // num_buckets
    x_offset = term_width // num_buckets
    
    screen.fill((0,0,0))
    
    for i, channel in enumerate(channel_data):
        buckets = []
        for bucket in range(num_buckets+1):
            vals = []
            for val in range(bucket*stepsize, (bucket+1)*stepsize):
                vals.append(channel[val])
                
            # Now we want to normalize all those values to between 0 and the maximum we can print 
            # And then sum them up
            lower = 0
            upper = term_height
            val_sum = (math.fsum( normalize(lower, upper, vals) ) / len(vals)) if len(vals) > 0 else 0
            buckets.append(int(val_sum))
        pygame.draw.lines(screen, COLORS[i%len(COLORS)], False, [(x*x_offset + ((1 - scale)/2)*screen_width, screen_height - (y + ((1 - scale)/2)*screen_height)) for x,y in enumerate(buckets)], 2)
    pygame.display.flip()
        
if __name__ == '__main__':
    
    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{}: {}".format(i, s))
        
    speaker_choice = int(input("Please enter the number of the speakers you want to use> "))
    speaker_name = selections[speaker_choice].name
    
    mixin = sc.get_microphone(id=speaker_name, include_loopback=True)

    with mixin.recorder(samplerate=SAMPLERATE) as rec:
        
        pygame.init()
        screen = pygame.display.set_mode((1280,480), pygame.RESIZABLE)
        
        clock = pygame.time.Clock()
        
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

            display_loop(screen, rec)
            clock.tick(120)
