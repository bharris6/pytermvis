import soundcard

from pytermvis.samplers.sampler import Sampler


class SoundcardSampler(Sampler):
    def __init__(self, rate=44100, period=1024, *args, **kwargs):
        Sampler.__init__(self, rate, period, *args, **kwargs)

        # Query for which card/device to use
        selections = soundcard.all_microphones(include_loopback=True)
        for i, d in enumerate(selections):
            print("{}: {}".format(i, d))

        device = int(input("Please enter the number of the device to use: "))
        device_name = selections[device].name

        # Instantiate the soundcard mixin
        self._mixin = soundcard.get_microphone(
            id=device_name,
            include_loopback=True,
        )

    def sample(self):
        # soundcard returns samples in a numpy array of frames x channels with
        # type of float32 and a range of [-1,1]
        with self._mixin.recorder(samplerate=self._rate) as rec:
            while True:
                frames = rec.record(numframes=self._period)
                yield frames
