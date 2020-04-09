import math

import pygame

COLORS = [ (255, 0, 0), (0, 255, 0), (0, 0, 255) ]


class PygameRenderer(object):

    def __init__(self, rgen, char="*"):
        self._rgen = rgen
        self._char = char


    def render(self, screen):
        frq, channel_data = next(self._rgen)

        screen_width, screen_height = pygame.display.get_surface().get_size()

        # Want to adjust to be a little less than fullscreen
        scale = 0.9
        term_width = scale * screen_width
        term_height = scale * screen_height

        num_buckets = 120

        # frq is the "x" that we want to plot
        stepsize = len(frq) // num_buckets
        x_offset = term_width // num_buckets

        screen.fill((0,0,0,))

        for i, channel in enumerate(channel_data):
            buckets = []
            for bucket in range(num_buckets+1):
                vals = []
                for val in range(bucket*stepsize, (bucket+1)*stepsize):
                    vals.append(channel[val])

                val_sum = (math.fsum([(0 + (term_height - 0)*v) for v in vals]) / len(vals)) if len(vals) > 0 else 0
                buckets.append( int(val_sum) )

            pygame.draw.lines(screen, COLORS[i % len(COLORS)], False, [(x*x_offset + ((1 - scale)/2)*screen_width, screen_height - (y + ((1 - scale)/2)*screen_height)) for x,y in enumerate(buckets)], 2)
        
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
