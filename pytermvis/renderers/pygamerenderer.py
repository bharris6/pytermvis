import math

import pygame

import numpy as np

from pytermvis.common import common

COLORS = [ (255, 0, 0), (0, 255, 0), (0, 0, 255) ]


class PygameRenderer(object):

    def __init__(self, rgen, char="*"):
        self._rgen = rgen
        self._char = char


    def render(self, screen):
        frq, channel_data = next(self._rgen)
        if len(frq) < 2:
            return

        screen_width, screen_height = pygame.display.get_surface().get_size()

        screen.fill((0,0,0,))

        num_bins = 512

        for i, channel in enumerate(channel_data):
            # Separate the channel into buckets
            channel_binned = common.to_bins(channel, num_bins)

            # Remap the values of x onto the screen width and y onto the screen height
            channel_length = len(channel_binned)
            xs = [common.remap(x, 0, channel_length, 0, screen_width) for x in range(0, channel_length)]
            ys = [common.remap(y, 0, 1, 0, screen_height*.75) for y in channel_binned]
            
            # draw on screen
            pygame.draw.lines(screen, COLORS[i%len(COLORS)], False, [(xs[x], (screen_height*0.9)-y) for x,y in enumerate(ys)], 2)

        pygame.display.flip()


    def start_render_loop(self):
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

            self.render(screen)
            clock.tick(120)
