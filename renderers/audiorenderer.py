from asciimatics.renderers import DynamicRenderer

class RandomTextRenderer(DynamicRenderer):

    def __init__(self, height, width, *args, **kwargs):
        super(RandomTextRenderer, self).__init__(height, width, *args, **kwargs)
        print("New Renderer!")


    def _write_line(self, x1, y1, x2, y2, char="*"):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self._write(char, x, y)
    
    def _render_now(self):
        self._clear()

        for i in range(10):
            x = random.randint(0, self._width)
            y = random.randint(0, self._height)
            x2 = random.randint(0, self._width)
            y2 = random.randint(0, self._height)
            self._write_line(x, y, x2, y2)

        return self._plain_image, self._colour_map

if __name__ == '__main__':
    
    import random, time
    from asciimatics.screen import Screen, ManagedScreen
    
    with ManagedScreen() as screen:
        height, width = screen.dimensions
        renderer = RandomTextRenderer(height, width)
        for i in range(10):
            print("{} : {}".format(i, renderer))
            time.sleep(1)
