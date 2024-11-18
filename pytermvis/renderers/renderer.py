from pytermvis.common.constants import RENDERER


class Renderer(object):

    @staticmethod
    def get_renderer(render_type=None, *args, **kwargs):
        if render_type == RENDERER.MATPLOTLIB:
            from .matplotlibrenderer import MatplotlibRenderer as renderer
        elif render_type == RENDERER.TEXT:
            from .textrenderer import TextRenderer as renderer
        elif render_type == RENDERER.ASCIIMATICS:
            from .asciimaticsrenderer import AsciimaticsRenderer as renderer
        elif render_type == RENDERER.PYGAME:
            from .pygamerenderer import PygameRenderer as renderer
        else:
            raise NotImplementedError(
                "Renderer {} not implemented.".format(render_type)
            )
        return renderer(*args, **kwargs)
