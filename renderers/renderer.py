__renderers = [ "asciimatics", "pygame" ]

class Renderer(object):

    @staticmethod
    def get_renderer(render_type=None, *args, **kwargs):
        if not render_type or render_type.lower() == "asciimatics":
            from .asciimaticsrenderer import AsciimaticsRenderer
            return AsciimaticsRenderer(*args, **kwargs)
        elif render_type.lower() == "pygame":
            from .pygamerenderer import PygameRenderer
            return PygameRenderer(*args, **kwargs)
