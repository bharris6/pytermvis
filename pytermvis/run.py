import argparse

from pytermvis.common.constants import (
    MODE,
    RENDERER,
    SAMPLER,
)

from pytermvis.samplers.sampler import Sampler
from pytermvis.renderers.renderer import Renderer


def main():

    description = "pytermvis -- Python audio visualizer"
    parser = argparse.ArgumentParser(description=description)

    # sample rate, period, mode
    parser.add_argument(
        "-s",
        "--sampler",
        type=SAMPLER,
        choices=[b for b in SAMPLER],
        default=SAMPLER.SOUNDCARD,
        help="Which backend sampler to use.",
    )

    parser.add_argument(
        "-r",
        "--renderer",
        type=RENDERER,
        choices=[r for r in RENDERER],
        default=RENDERER.TEXT,
        help="Choose which renderer to use.",
    )

    parser.add_argument(
        "--rate",
        type=int,
        default=44100,
        required=False,
        help="Sample rate for sampling audio.",
    )

    parser.add_argument(
        "--period",
        type=int,
        default=1024,
        required=False,
        help="How many frames per sample",
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=MODE,
        choices=[m for m in MODE],
        default=MODE.AUDIO,
        help="What visualization to show."
    )

    args = parser.parse_args()

    sampler = Sampler.get_sampler(
        args.sampler,
        args.rate,
        args.period,
    )

    renderer = Renderer.get_renderer(
        args.renderer,
        args.rate,
        args.period,
        sampler.sample(),
        args.mode,
    )

    renderer.start_render_loop()


if __name__ == '__main__':
    main()
