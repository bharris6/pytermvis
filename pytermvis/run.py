import argparse, math, os, sys, time

from pytermvis.renderers.renderer import Renderer


def main():

    SAMPLERATE = 44100
    CHARACTER="*"
    CHANNELS = 2

    parser = argparse.ArgumentParser(description="pytermvis -- Python Terminal Visualizer")

    parser.add_argument("-c", "--char", action="store", dest="char", default=CHARACTER)
    parser.add_argument("-s", "--sample-rate", action="store", dest="samplerate", default=SAMPLERATE)
    parser.add_argument("-b", "--backend", action="store", dest="backend", default="soundcard")
    parser.add_argument("-r", "--renderer", action="store", dest="rendertype", default="text")

    parser_args = parser.parse_args()

    SAMPLERATE = int(parser_args.samplerate)
    
    if parser_args.backend.lower() == "alsa":
        from pytermvis.samplers.alsasampler import AlsaSampler
        sampler = AlsaSampler(rate=SAMPLERATE, cardindex=1)
    elif parser_args.backend.lower() == "soundcard":
        from pytermvis.samplers.soundcardsampler import SoundcardSampler
        sampler = SoundcardSampler(rate=SAMPLERATE)
        sampler.start()

    renderer = Renderer.get_renderer(parser_args.rendertype, sampler.samplegen(), parser_args.char)
    renderer.start_render_loop()


if __name__ == '__main__':
    main()
