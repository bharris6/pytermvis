# pytermvis
Terminal Audio Visualizer

## Requirements

* asciimatics
* numpy
* scipy
* [SoundCard](https://github.com/bastibe/SoundCard)

## How to install

```
$ git clone https://github.com/bharris6/pytermvis.git
$ cd pytermvis
$ pip install --user -r requirements.txt
```

## How to run

```
$ python asciimatics_vis.py
```

This will query your local system to determine what sound devices exist, and prompt you to choose one.  All visualizer output is in the same terminal.  

## What does it do?

`pytermvis` uses `SoundCard`'s ability to record from "loopback" devices.  This means it is basically catching the audio output of your speaker and passing those raw frames through `numpy`'s/`scipy`'s FFT to get the frequency domain representation.  Then, that FFT data is split into buckets based on the terminal width and each bucket's amplitude is printed as vertical lines using `asciimatics`.

## Issues

Requires PulseAudio for now on Linux.  


