from pytermvis.common.constants import RENDERER


class Renderer(object):

    @staticmethod
    def get_renderer(render_type=None, *args, **kwargs):
        if render_type == RENDERER.MATPLOTLIB:
            from .matplotlibrenderer import MatplotlibRenderer
            return MatplotlibRenderer(*args, **kwargs)
        elif render_type == RENDERER.TEXT:
            from .textrenderer import TextRenderer
            return TextRenderer(*args, **kwargs)
        else:
            raise NotImplementedError(
                "Renderer {} not implemented.".format(render_type)
            )
