__renderers = [ "asciimatics", "audio", "pygame" ]

class Renderer(object):

    @staticmethod
    def get_renderer(render_type=None, *args, **kwargs):
        if not render_type or render_type.lower() == "text":
            from .audiorenderer import AudioRenderer
            return AudioRenderer(*args, **kwargs)
        elif render_type.lower() == "pygame":
            from .pygamerenderer import PygameRenderer
            return PygameRenderer(*args, **kwargs)
        elif render_type.lower() == "asciimatics":
            from .asciimaticsrenderer import AsciimaticsRenderer
            return AsciimaticsRenderer(*args, **kwargs)
            
