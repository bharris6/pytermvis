import argparse, math, os, sys, time

import soundcard as sc

from common import samplegen
from renderers.asciimaticsrenderer import AsciimaticsRenderer

SAMPLERATE = 44100
CHARACTER="*"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="pytermvis -- Python Terminal Visualizer")

    parser.add_argument("-c", "--char", action="store", dest="char", default=CHARACTER)
    parser.add_argument("-s", "--sample-rate", action="store", dest="samplerate", default=SAMPLERATE)
    parser.add_argument("-r", "--renderer", action="store", dest="rendertype", default="asciimatics")

    parser_args = parser.parse_args()

    SAMPLERATE = int(parser_args.samplerate)
    
    selections = sc.all_speakers()
    for i, s in enumerate(selections):
        print("{}: {}".format(i, s))
        
    speaker_choice = int(input("Please enter the number of the speakers you want to use> "))
    speaker_name = selections[speaker_choice].name
    
    mixin = sc.get_microphone(id=speaker_name, include_loopback=True)

    with mixin.recorder(samplerate=SAMPLERATE) as rec:
        renderer = AsciimaticsRenderer(None, samplegen(rec), parser_args.char)
        renderer.start_render_loop()

